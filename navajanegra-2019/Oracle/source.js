const fs = require('fs');
const express = require('express');
const session = require('express-session')
const cookieParser = require('cookie-parser');
const { URL } = require('url');
const uuidv4 = require('uuid/v4');
const path = require('path');
const bot = require('./bot');
const crypto = require('crypto');
const mariadb = require('mariadb');

const server = process.env.SERVER || 'http://localhost';
const port = process.env.PORT || 3333;
const flag = process.env.FLAG || 'nn9ed{wololo}';

const db = require('./config');
const pool = mariadb.createPool(db);

const render = function(file, obj) {
	let data = fs.readFileSync(path.join(__dirname, file)).toString();
	for (let [k,v] of Object.entries(obj)) {
		data = data.replace(new RegExp('{{ ' + k + ' }}', 'g'), v);
	}
	return data;
}

const app = express();

(async () => {
	let conn;
	try {
		conn = await pool.getConnection();
		console.log('[+] Creating database');
		let ret = await conn.query('CREATE TABLE IF NOT EXISTS challenge (flag VARCHAR(255), bait VARCHAR(255));');
		ret = await conn.query('CREATE TABLE IF NOT EXISTS admin (user VARCHAR(255), password VARCHAR(32));');
		await conn.query('CREATE TABLE IF NOT EXISTS html (id VARCHAR(36), html LONGTEXT);');
		await conn.query(`INSERT INTO challenge (flag, bait) VALUES ("${flag}", "Season 6, Episode 16");`);
		await conn.query('INSERT INTO challenge (flag, bait) VALUES ("Nope", "nn9ed{undefined}");');
		await conn.query('INSERT INTO challenge (flag, bait) VALUES ("Bender", "Hey sexy mama. Wanna kill all humans?");');
		await conn.query('INSERT INTO challenge (flag, bait) VALUES ("Wat", "That’ll teach those other horses to take drugs.");');
	} catch (err) {
		throw err;
	} finally {
		if (conn) return conn.end();
	}
})();

app.use(function(req, res, next) {
    res.setHeader('X-Content-Type-Options', 'nosniff');
	next();
});

app.use(express.urlencoded({extended: false}));
app.use(express.json());
app.use(cookieParser());
app.use(session({
  secret: crypto.randomBytes(16).toString('hex'),
  resave: true,
  saveUninitialized: true,
  cookie: { secure: false }
}))

app.use(express.static(path.join(__dirname, 'static')))

app.get('/admin', function (req, res, next) {
	// check authentication
	if (!req.session.is_admin) {
		return res.sendFile(path.join(__dirname, 'templates/login.html'));
	}
	return res.sendFile(path.join(__dirname, 'templates/admin.html'));
});

async function is_admin(user, pwd) {
	let res = [], conn;
	try {
		conn = await pool.getConnection();
		res = await conn.query('SELECT * from admin WHERE user = ? AND password = ?', [user, pwd]);
	} catch (e) { } finally {
		if (conn) conn.end();
	}
	if (res.length == 0) {
		return false;
	} else {
		return true;
	}
}

app.post('/admin', async function (req, res) {
	let user = req.body.user, pwd = req.body.pass;
	let admin = await is_admin(user, pwd);
	if (admin) {
		req.session.is_admin = true;
		return res.sendFile(path.join(__dirname, 'templates/admin.html'));
	} else {
		return res.sendFile(path.join(__dirname, 'templates/login.html'));
	}
});

app.get('/admin/search/:query', async function (req, res) {
	if (!req.session.is_admin) {
		return res.sendStatus(401);
	} else {
		let conn;
		try {
			conn = await pool.getConnection();
			let row = await conn.query('SELECT bait FROM challenge WHERE bait LIKE \'%' + req.params.query + '%\'');
			res.json(row);
		} catch (e) {
			res.sendStatus(400);
		} finally {
			if (conn) return conn.end();
		}
	}
});

app.post('/createhtml', async function (req, res) {
	let html = req.body.html;
	if (!html) return res.sendStatus(400);
	let secret = uuidv4();
	let conn;
	try {
		conn = await pool.getConnection();
		let ret = await conn.query('INSERT INTO html (id, html) VALUES (?,?)', [secret, html]);
		res.send(render('templates/created.html', { uid: secret }));
	} catch (e) {
		res.sendStatus(400);
	} finally {
		if (conn) return conn.end();
	}
});

app.get('/readhtml/:uid', async function (req, res) {
	let uid = req.params.uid;
	let conn;
	try {
		conn = await pool.getConnection();
		let row = await conn.query('SELECT html FROM html WHERE id = ?', [uid]);
		if (row.length == 0) {
			return res.sendStatus(404);
		}
		res.setHeader('Content-Security-Policy', "default-src 'self' 'unsafe-inline'; img-src *; style-src *; font-src *");
		res.send(render('templates/read.html', {uid: uid, content: row[0].html}));
	} catch (e) {
		res.sendStatus(404);
	} finally {
		if (conn) return conn.end();
	}
});

app.get('/report/:uid', async function (req, res) {
	// check that uid exists
	let uid = req.params.uid, conn;
	try {
		conn = await pool.getConnection();
		let row = await conn.query('SELECT html FROM html WHERE id = ?', [uid]);
		if (row.length == 0) {
			// send url to bot
			let url = `${server}:${port}/readhtml/${uid}`;
			bot.visitUrl(url);
			res.sendFile(path.join(__dirname, 'templates/reported.html'));
		}
	} catch (e) {
		res.sendStatus(404);
	} finally {
		if (conn) return conn.end();
	}
});

app.get('/', function (req, res) {
    return res.sendFile(path.join(__dirname, 'templates/index.html'));
});

app.get('*', function (req, res) {
	res.redirect('/');
});

app.listen(port, function () {
    console.log('[+] Listening at port ' + port)
	bot.init(server, port); // start admin bot
});

