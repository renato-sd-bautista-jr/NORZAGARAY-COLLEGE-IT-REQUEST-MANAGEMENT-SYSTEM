from flask import render_template, request, redirect, url_for, session,Flask
from manage_item import get_devices_with_details, add_device
from manage_user import get_user, edit_user, delete_user
from login import login_bp

app = Flask(__name__)
app.secret_key = 'a2f1e4f8f60b4f81a8d32dd0b3c2ce90'
app.register_blueprint(login_bp)

@app.route('/')
def index():
    # always go to login if not logged in
    if 'user_id' not in session:
        return redirect(url_for('login_bp.login'))
    # or redirect to admin if logged in
    return redirect(url_for('admin'))
@app.route('/admin')
def admin():
    if 'user_id' not in session:  # not logged in
        return redirect(url_for('login_bp.login'))
    if not session.get('is_admin'):
        # if user tries to access admin but isn't admin, redirect them
        return redirect(url_for('concernlist'))

    return render_template('admin.html', username=session.get('username'))
@app.route('/concernlist')
def concernlist():
    if 'user_id' not in session:
        return redirect(url_for('login_bp.login'))
    return render_template('concernlist.html', username=session.get('username'))


@app.route('/manage-user')
def manage_user():
    if 'user_id' not in session:
        return redirect(url_for('login_bp.login'))

    all_users = get_user()
    return render_template('manage_user.html', users=all_users)

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')


@app.route('/manage-item', methods=['GET', 'POST'])
def manage_item():
    if 'user_id' not in session:  # block unauthorized users
        return redirect(url_for('login_bp.login'))

    if request.method == 'POST':
        # Example: add a new device from form
        device_name = request.form.get('item_name')
        quantity = request.form.get('quantity')
        department_id = 1  # or from form if you let user select department
        add_device(device_name, quantity, department_id)
        return redirect(url_for('manage_item'))

    items = get_devices_with_details()
    return render_template('manage_item.html', items=items)


@app.route('/edit-item/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    # logic to edit the item goes here
    return f"Edit item {id}"  # placeholder for now

@app.route('/delete-item/<int:id>', methods=['POST'])
def delete_item(id):
    # logic to delete the item goes here
    return redirect(url_for('manage_item'))

if __name__ == "__main__":
    app.run(debug=True)
