import sys
import copy
from distutils import util
from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental.db'
db = SQLAlchemy(app)


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    idem_product_id = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    product_name = db.Column(db.String(80), nullable=True)
    product_description = db.Column(db.String(200), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Product ID %r' % self.product_id


class Businesspartner(db.Model):
    bpartner_id = db.Column(db.Integer, primary_key=True)
    idem_bpartner_id = db.Column(db.String(20), nullable=False)
    bpname = db.Column(db.String(80), nullable=True)
    ctfirstname = db.Column(db.String(80), nullable=True)
    ctlastname = db.Column(db.String(80), nullable=True)
    bpplace = db.Column(db.String(80), nullable=True)
    bpzip = db.Column(db.String(8), nullable=True)
    bpcountry = db.Column(db.String(80), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<BPartner ID %r' % self.bpartner_id


class Contract(db.Model):
    contract_id = db.Column(db.Integer, primary_key=True)
    bpartner_name = db.Column(db.String(80), nullable=True)
    product_name = db.Column(db.String(80), nullable=True)
    startdate = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Integer, nullable=True)  # total number of rental months including the initial_fee
    currency = db.Column(db.String(3), nullable=True)
    initial_fee = db.Column(db.Numeric, nullable=True)
    regular_fee = db.Column(db.Numeric, nullable=True)
    purch_amnt = db.Column(db.Numeric, nullable=True)
    cancelled = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Contract ID %r' % self.contract_id


# ROUTER FOR PRODUCT MANAGMENT

@app.route('/prod', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        product_idemid = request.form['idemid']
        product_prodname = request.form['prodname']
        product_proddescription = request.form['proddescription']
        new_product = Product(
            idem_product_id=product_idemid,
            product_name=product_prodname,
            product_description=product_proddescription)

        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect('/prod')
        except:
            return 'There was an issue adding the product'

    else:
        products = Product.query.order_by(Product.product_name).all()
        return render_template('prod/index.html', products=products)


@app.route('/setinactive/<int:product_id>')
def setinactive(product_id):
    product_to_setinactive = Product.query.get_or_404(product_id)

    try:
        db.session.delete(product_to_setinactive)
        db.session.commit()
        return redirect('/prod')
    except:
        return 'There was a problem deleting the product'


@app.route('/update/<int:product_id>', methods=['GET', 'POST'])
def update(product_id):
    product_to_update = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product_to_update.idem_product_id = request.form['idemid']
        product_to_update.product_name = request.form['prodname']
        product_to_update.product_description = request.form['proddescription']

        try:
            db.session.commit()
            return redirect('/prod')
        except:
            return 'There was a problem updating the product'
    else:
        return render_template('prod/update.html', product=product_to_update)


# ROUTER FOR BUSINESS-PARTNER MANAGMENT

@app.route('/bpartner', methods=['POST', 'GET'])
def bpindex():
    if request.method == 'POST':
        bp_idemid = request.form['idemid']
        bp_bpname = request.form['bpname']
        bp_ctfirstname = request.form['ctfirstname']
        bp_ctlastname = request.form['ctlastname']
        bp_place = request.form['bpplace']
        bp_zip = request.form['bpzip']
        bp_country = request.form['bpcountry']
        new_bpartner = Businesspartner(
            idem_bpartner_id=bp_idemid,
            bpname=bp_bpname,
            ctfirstname=bp_ctfirstname,
            ctlastname=bp_ctlastname,
            bpplace=bp_place,
            bpzip=bp_zip,
            bpcountry=bp_country)

        try:
            db.session.add(new_bpartner)
            db.session.commit()
            return redirect('/bpartner')
        except:
            return 'There was an issue adding the business partner'

    else:
        bpartners = Businesspartner.query.order_by(
            Businesspartner.ctlastname).all()
        return render_template('bpartner/index.html', bpartners=bpartners)


@app.route('/bpsetinactive/<int:bpartner_id>')
def bpsetinactive(bpartner_id):
    bpartner_to_setinactive = Businesspartner.query.get_or_404(bpartner_id)

    try:
        db.session.delete(bpartner_to_setinactive)
        db.session.commit()
        return redirect('/bpartner')
    except:
        return 'There was a problem deleting the business partner'


@app.route('/bpupdate/<int:bpartner_id>', methods=['GET', 'POST'])
def bpupdate(bpartner_id):
    bpartner_to_update = Businesspartner.query.get_or_404(bpartner_id)

    if request.method == 'POST':
        bpartner_to_update.idem_bpartner_id = request.form['idemid']
        bpartner_to_update.bpname = request.form['bpname']
        bpartner_to_update.ctfirstname = request.form['ctfirstname']
        bpartner_to_update.ctlastname = request.form['ctlastname']
        bpartner_to_update.bpplace = request.form['bpplace']
        bpartner_to_update.bpzip = request.form['bpzip']
        bpartner_to_update.bpcountry = request.form['bpcountry']

        try:
            db.session.commit()
            return redirect('/bpartner')
        except:
            return 'There was a problem updating the business partner'
    else:
        return render_template(
            'bpartner/update.html', bpartner=bpartner_to_update
            )


# ROUTER FOR CONTRACT MANAGMENT

@app.route('/contract', methods=['POST', 'GET'])
def cindex():
    if request.method == 'POST':
        cbpartner_name = request.form['bpartner_name']
        cproduct_name = request.form['product_name']
        cstartdate = datetime.strptime(request.form['startdate'], "%d.%m.%Y")
        cduration = request.form['duration']
        ccurrency = request.form['currency']
        cinitial_fee = request.form['initial_fee']
        cregular_fee = request.form['regular_fee']
        cpurch_amnt = request.form['purch_amnt']
        try:
            if request.form['cancelled'] == "on":
                ccancelled = True
        except:
            ccancelled = False
        try:
            if request.form['completed'] == "on":
                ccompleted = True
        except:
            ccompleted = False
        new_contract = Contract(
            bpartner_name=cbpartner_name,
            product_name=cproduct_name,
            startdate=cstartdate,
            duration=cduration,
            currency=ccurrency,
            initial_fee=cinitial_fee,
            regular_fee=cregular_fee,
            purch_amnt=cpurch_amnt,
            cancelled=ccancelled,
            completed=ccompleted)

        try:
            db.session.add(new_contract)
            db.session.commit()
            return redirect('/contract')
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print("ERROR: ", error)
            return 'There was an issue adding the contract', error

    else:
        products = Product.query.order_by(
            Product.product_name).all()

        bpartners = Businesspartner.query.order_by(
            Businesspartner.bpname).all()

        contracts = Contract.query.order_by(
            Contract.startdate.desc()).all()
        for c in contracts:
            c.startdate = datetime.strftime(c.startdate, "%d.%m.%Y")
            c.duration = str(c.duration)
            c.initial_fee = '{:,.2f}'.format(c.initial_fee)
            c.regular_fee = '{:,.2f}'.format(c.regular_fee)
            c.purch_amnt = '{:,.2f}'.format(c.purch_amnt)
            c.cancelled = str(c.cancelled)
            c.completed = str(c.completed)

        return render_template('contract/index.html', contracts=contracts, products=products, bpartners=bpartners)


@app.route('/contractsetinactive/<int:contract_id>')
def contractsetinactive(contract_id):
    contract_to_setinactive = Contract.query.get_or_404(contract_id)

    try:
        db.session.delete(contract_to_setinactive)
        db.session.commit()
        return redirect('/contract')
    except:
        return 'There was a problem deleting the contract'


@app.route('/contractupdate/<int:contract_id>', methods=['GET', 'POST'])
def contractupdate(contract_id):
    contract_to_update = Contract.query.get_or_404(contract_id)

    if request.method == 'POST':
        contract_to_update.bpartner_name = request.form['bpartner_name']
        contract_to_update.product_name = request.form['product_name']
        contract_to_update.startdate = datetime.strptime(request.form['startdate'], "%d.%m.%Y")
        contract_to_update.duration = request.form['duration']
        contract_to_update.currency = request.form['currency']
        contract_to_update.initial_fee = request.form['initial_fee']
        contract_to_update.regular_fee = request.form['regular_fee']
        contract_to_update.purch_amnt = request.form['purch_amnt']
        contract_to_update.cancelled = util.strtobool(request.form['cancelled'])
        contract_to_update.completed = util.strtobool(request.form['completed'])

        try:
            db.session.commit()
            return redirect('/contract')
        except:
            return 'There was a problem updating the contract'
    else:
        bpartners = Businesspartner.query.order_by(
            Businesspartner.bpname).all()

        products = Product.query.order_by(
            Product.product_name).all()

        contract_to_update.startdate = datetime.strftime(contract_to_update.startdate, "%d.%m.%Y")
        contract_to_update.duration = str(contract_to_update.duration)
        contract_to_update.initial_fee = '{:.2f}'.format(contract_to_update.initial_fee)
        contract_to_update.regular_fee = '{:.2f}'.format(contract_to_update.regular_fee)
        contract_to_update.purch_amnt = '{:.2f}'.format(contract_to_update.purch_amnt)
        contract_to_update.cancelled = str(contract_to_update.cancelled)
        contract_to_update.completed = str(contract_to_update.completed)

        return render_template('contract/update.html', contract=contract_to_update, products=products, bpartners=bpartners)


# ROUTER FOR CONTRACT-ROWS (line-items, calculated from CONTRACT header)

@app.route('/contractrows/<int:contract_id>', methods=['POST', 'GET'])
def rindex(contract_id):
    cheader = Contract.query.get_or_404(contract_id)
    header = copy.copy(cheader)
    header.startdate = datetime.strftime(header.startdate, "%a, %d.%m.%Y")

    class Contractrow(object):
        def __init__(self, instalment, type, invoicedate, amount, totalpaid, balance, past, present):
            self.instalment = instalment
            self.type = type
            self.invoicedate = invoicedate
            self.amount = amount
            self.totalpaid = totalpaid
            self.balance = balance
            self.past = past
            self.present = present

    rows = []

    # compute total amount
    totalamount = cheader.initial_fee
    for r in range(cheader.duration-1):
        totalamount += cheader.regular_fee
    totalamount += cheader.purch_amnt

    # first lease payment
    instalment = 1
    totalpaid = cheader.initial_fee
    payday = cheader.startdate
    amount = cheader.initial_fee
    balance = totalamount - amount
    past = False  # flag to set background color for months in the past in template
    present = False  # flag to highligh present month in template

    if payday.replace(day=1, hour=0, minute=0, second=0, microsecond=0) < datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0):
        past = True
    if payday.replace(day=1, hour=0, minute=0, second=0, microsecond=0) == datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0):
        present = True

    rows.append(Contractrow(str(instalment), "First", datetime.strftime(payday, "%a, %d.%m.%Y"), '{:,.2f}'.format(amount), '{:,.2f}'.format(totalpaid), '{:,.2f}'.format(balance), past, present))

    # regular lease payment
    for r in range(cheader.duration-1):
        instalment += 1
        amount = cheader.regular_fee
        totalpaid += amount
        payday = payday + relativedelta(months=1)
        payday = payday.replace(day=25)
        balance -= amount
        past = False
        present = False

        if datetime.strftime(payday, "%a") == "Sat":
            payday = payday - relativedelta(days=1)

        if datetime.strftime(payday, "%a") == "Sun":
            payday = payday - relativedelta(days=2)

        if payday.replace(day=1, hour=0, minute=0, second=0, microsecond=0) < datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0):
            past = True
        if payday.replace(day=1, hour=0, minute=0, second=0, microsecond=0) == datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0):
            present = True

        rows.append(Contractrow(str(instalment), "Regular", datetime.strftime(payday, "%a, %d.%m.%Y"), '{:,.2f}'.format(amount), '{:,.2f}'.format(totalpaid), '{:,.2f}'.format(balance), past, present))

    # final purchase
    instalment += 1
    payday = payday + relativedelta(months=1)
    payday = payday.replace(day=25)
    amount = cheader.purch_amnt
    totalpaid += amount
    balance -= amount
    past = False
    present = False

    if datetime.strftime(payday, "%a") == "Sat":
        payday = payday - relativedelta(days=1)
    if datetime.strftime(payday, "%a") == "Sun":
        payday = payday - relativedelta(days=2)

    if payday.replace(day=1, hour=0, minute=0, second=0, microsecond=0) < datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0):
        past = True
    if payday.replace(day=1, hour=0, minute=0, second=0, microsecond=0) == datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0):
        present = True

    rows.append(Contractrow(instalment, "Final Purchase", datetime.strftime(payday, "%a, %d.%m.%Y"), '{:,.2f}'.format(amount), '{:,.2f}'.format(totalpaid), '{:,.2f}'.format(balance), past, present))

    return render_template('contractrows/index.html', header=header, rows=rows)


# ROUTER FOR REPORT: INVOICERUN

@app.route('/reports/invoicerun', methods=['POST', 'GET'])
def invoicerun_index():

    class Invoicerun(object):
        def __init__(self, linenumber, product_name, bpartner_name, type, invoicedate, currency, amount, contract_id):
            self.linenumber = linenumber
            self.product_name = product_name
            self.bpartner_name = bpartner_name
            self.type = type
            self.invoicedate = invoicedate
            self.currency = currency
            self.amount = amount
            self.contract_id = contract_id

    contracts = Contract.query.order_by(
        Contract.bpartner_name, Contract.product_name, Contract.startdate).all()

    rows = []

    linenumber = 0

    invoiceruntotal = 0

    for c in contracts:
        # initial fee
        product_name = c.product_name
        bpartner_name = c.bpartner_name
        currency = c.currency
        amount = c.initial_fee
        type = "First"
        invoicedate = c.startdate
        if invoicedate.replace(day=1, hour=0, minute=0, second=0, microsecond=0) == datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0):
            linenumber += 1
            invoiceruntotal += amount
            rows.append(Invoicerun(linenumber, product_name, bpartner_name, type, datetime.strftime(invoicedate, "%a, %d.%m.%Y"), currency, '{:,.2f}'.format(amount), c.contract_id))

        # regular fee
        for r in range(c.duration-1):
            product_name = c.product_name
            bpartner_name = c.bpartner_name
            currency = c.currency
            amount = c.regular_fee
            type = "Regular"
            invoicedate = invoicedate + relativedelta(months=1)
            invoicedate = invoicedate.replace(day=25)
            if datetime.strftime(invoicedate, "%a") == "Sat":
                invoicedate = invoicedate - relativedelta(days=1)
            if datetime.strftime(invoicedate, "%a") == "Sun":
                invoicedate = invoicedate - relativedelta(days=2)
            if invoicedate.replace(day=1, hour=0, minute=0, second=0, microsecond=0) == datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0):
                linenumber += 1
                invoiceruntotal += amount
                rows.append(Invoicerun(linenumber, product_name, bpartner_name, type, datetime.strftime(invoicedate, "%a, %d.%m.%Y"), currency, '{:,.2f}'.format(amount), c.contract_id))

        # final purchase
        product_name = c.product_name
        bpartner_name = c.bpartner_name
        currency = c.currency
        amount = c.purch_amnt
        type = "Final Purchase"
        invoicedate = invoicedate + relativedelta(months=1)
        invoicedate = invoicedate.replace(day=25)
        if datetime.strftime(invoicedate, "%a") == "Sat":
            invoicedate = invoicedate - relativedelta(days=1)
        if datetime.strftime(invoicedate, "%a") == "Sun":
            invoicedate = invoicedate - relativedelta(days=2)
        if invoicedate.replace(day=1, hour=0, minute=0, second=0, microsecond=0) == datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0):
            linenumber += 1
            invoiceruntotal += amount
            rows.append(Invoicerun(linenumber, product_name, bpartner_name, type, datetime.strftime(invoicedate, "%a, %d.%m.%Y"), currency, '{:,.2f}'.format(amount), c.contract_id))

    month = datetime.strftime(datetime.now(), "%B, %Y")

    return render_template('reports/invoicerun/index.html', rows=rows, month=month, invoiceruntotal='{:,.2f}'.format(invoiceruntotal))


# ROUTER FOR REPORT: INVOICE FORECAST NEXT MONTH

@app.route('/reports/invoiceforecast', methods=['POST', 'GET'])
def invoiceforecast_index():

    class Invoicerun(object):
        def __init__(self, linenumber, product_name, bpartner_name, type, invoicedate, currency, amount, contract_id):
            self.linenumber = linenumber
            self.product_name = product_name
            self.bpartner_name = bpartner_name
            self.type = type
            self.invoicedate = invoicedate
            self.currency = currency
            self.amount = amount
            self.contract_id = contract_id

    contracts = Contract.query.order_by(
        Contract.product_name, Contract.bpartner_name, Contract.startdate).all()

    rows = []

    linenumber = 0

    invoiceruntotal = 0

    for c in contracts:
        # initial fee
        product_name = c.product_name
        bpartner_name = c.bpartner_name
        currency = c.currency
        amount = c.initial_fee
        type = "First"
        invoicedate = c.startdate
        if invoicedate.replace(day=1, hour=0, minute=0, second=0, microsecond=0) == datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) + relativedelta(months=+1):
            linenumber += 1
            invoiceruntotal += amount
            rows.append(Invoicerun(linenumber, product_name, bpartner_name, type, datetime.strftime(invoicedate, "%a, %d.%m.%Y"), currency, '{:,.2f}'.format(amount), c.contract_id))

        # regular fee
        for r in range(c.duration-1):
            product_name = c.product_name
            bpartner_name = c.bpartner_name
            currency = c.currency
            amount = c.regular_fee
            type = "Regular"
            invoicedate = invoicedate + relativedelta(months=1)
            invoicedate = invoicedate.replace(day=25)
            if datetime.strftime(invoicedate, "%a") == "Sat":
                invoicedate = invoicedate - relativedelta(days=1)
            if datetime.strftime(invoicedate, "%a") == "Sun":
                invoicedate = invoicedate - relativedelta(days=2)
            if invoicedate.replace(day=1, hour=0, minute=0, second=0, microsecond=0) == datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) + relativedelta(months=+1):
                linenumber += 1
                invoiceruntotal += amount
                rows.append(Invoicerun(linenumber, product_name, bpartner_name, type, datetime.strftime(invoicedate, "%a, %d.%m.%Y"), currency, '{:,.2f}'.format(amount), c.contract_id))

        # final purchase
        product_name = c.product_name
        bpartner_name = c.bpartner_name
        currency = c.currency
        amount = c.purch_amnt
        type = "Final Purchase"
        invoicedate = invoicedate + relativedelta(months=1)
        invoicedate = invoicedate.replace(day=25)
        if datetime.strftime(invoicedate, "%a") == "Sat":
            invoicedate = invoicedate - relativedelta(days=1)
        if datetime.strftime(invoicedate, "%a") == "Sun":
            invoicedate = invoicedate - relativedelta(days=2)
        if invoicedate.replace(day=1, hour=0, minute=0, second=0, microsecond=0) == datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) + relativedelta(months=+1):
            linenumber += 1
            invoiceruntotal += amount
            rows.append(Invoicerun(linenumber, product_name, bpartner_name, type, datetime.strftime(invoicedate, "%a, %d.%m.%Y"), currency, '{:,.2f}'.format(amount), c.contract_id))

    month = datetime.strftime(datetime.now() + relativedelta(months=+1), "%B, %Y")

    return render_template('reports/invoiceforecast/index.html', rows=rows, month=month, invoiceruntotal='{:,.2f}'.format(invoiceruntotal))


# ROUTER FOR REPORT: finals next month

@app.route('/reports/finalsnextmonth', methods=['POST', 'GET'])
def reportsfinalindex():

    class Finals(object):
        def __init__(self, linenumber, product_name, bpartner_name, type, invoicedate, currency, amount, contract_id):
            self.linenumber = linenumber
            self.product_name = product_name
            self.bpartner_name = bpartner_name
            self.type = type
            self.invoicedate = invoicedate
            self.currency = currency
            self.amount = amount
            self.contract_id = contract_id

    contracts = Contract.query.order_by(
        Contract.product_name, Contract.bpartner_name, Contract.startdate).all()

    rows = []

    linenumber = 0

    invoiceruntotal = 0

    for c in contracts:
        # initial fee
        product_name = c.product_name
        bpartner_name = c.bpartner_name
        currency = c.currency
        amount = c.initial_fee
        type = "First"
        invoicedate = c.startdate
        if invoicedate.replace(day=1, hour=0, minute=0, second=0, microsecond=0) == datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) + relativedelta(months=+1) and type == "Final Purchase":
            linenumber = 1
            invoiceruntotal=amount
            rows.append(Finals(linenumber, product_name, bpartner_name, type, datetime.strftime(invoicedate, "%a, %d.%m.%Y"), currency, '{:,.2f}'.format(amount), c.contract_id))

        # regular fee
        for r in range(c.duration-1):
            product_name = c.product_name
            bpartner_name = c.bpartner_name
            currency = c.currency
            amount = c.regular_fee
            type = "Regular"
            invoicedate = invoicedate + relativedelta(months=1)
            invoicedate = invoicedate.replace(day=25)
            if datetime.strftime(invoicedate, "%a") == "Sat":
                invoicedate = invoicedate - relativedelta(days=1)
            if datetime.strftime(invoicedate, "%a") == "Sun":
                invoicedate = invoicedate - relativedelta(days=2)
            if invoicedate.replace(day=1, hour=0, minute=0, second=0, microsecond=0) == datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) + relativedelta(months=+1) and type == "Final Purchase":
                linenumber += 1
                invoiceruntotal += amount
                rows.append(Finals(linenumber, product_name, bpartner_name, type, datetime.strftime(invoicedate, "%a, %d.%m.%Y"), currency, '{:,.2f}'.format(amount), c.contract_id))

        # final purchase
        product_name = c.product_name
        bpartner_name = c.bpartner_name
        currency = c.currency
        amount = c.purch_amnt
        type = "Final Purchase"
        invoicedate = invoicedate + relativedelta(months=1)
        invoicedate = invoicedate.replace(day=25)
        if datetime.strftime(invoicedate, "%a") == "Sat":
            invoicedate = invoicedate - relativedelta(days=1)
        if datetime.strftime(invoicedate, "%a") == "Sun":
            invoicedate = invoicedate - relativedelta(days=2)
        if invoicedate.replace(day=1, hour=0, minute=0, second=0, microsecond=0) == datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) + relativedelta(months=+1) and type == "Final Purchase":
            linenumber += 1
            invoiceruntotal += amount
            rows.append(Finals(linenumber, product_name, bpartner_name, type, datetime.strftime(invoicedate, "%a, %d.%m.%Y"), currency, '{:,.2f}'.format(amount), c.contract_id))

    month = datetime.strftime(datetime.now(), "%B, %Y")

    return render_template('reports/finalsnextmonth/index.html', rows=rows, month=month, invoiceruntotal='{:,.2f}'.format(invoiceruntotal))


@app.route('/reports', methods=['POST', 'GET'])
def reportsindex():
    return render_template('/reports/index.html')


@app.route('/', methods=['POST', 'GET'])
def mindex():
    return render_template('/index.html')


if __name__ == "__main__":
    app.run(debug=True)
