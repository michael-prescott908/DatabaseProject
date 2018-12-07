const express = require('express');
const cors = require('cors');
const mysql = require('mysql');

const app = express();

const SELECT_All_STUDENTS = 'SELECT * FROM STUDENTS';

const connection = mysql.createConnection({
    host: 'db.summersend.serverswc.com',
    user: 'michael',
    password: 'databaseproject',
    database: 'dbproject'
});

connection.connect(err => {
    if(err){
        console.log('Something went wrong': err);
        return err;
    }
});

app.use(cors());

app.get('/', (req, res) => {
    res.send('hello from the students server')
});

app.get('/students/add', (req, res) => {
    console.log('I am adding a student');
    const { ID, FirstName, MiddleName, LastName } = req.query;
    const INSERT_STUDENT = `INSERT INTO Students (ID, FirstName, MiddleName, LastName) ` +
    `VALUES (${ID}, '${FirstName}', '${MiddleName}', '${LastName}')`
    console.log(ID, FirstName, MiddleName, LastName);
    connection.query(INSERT_STUDENT, (err, results) => {
        if(err){
            return res.send(err)
        }
        else {
            return res.send('Student was added')
        }
    });
});

app.get('/students', (req, res) => {
    connection.query(SELECT_All_STUDENTS, (err, results) => {
        if(err) {
            return res.send(err)
        }
        else {
            return res.json({
                data: results
            })
        }
    });
});

app.listen(4000, () => {
    console.log('Products server listening on ' +
    'port 4000')
});
