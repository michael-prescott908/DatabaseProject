import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {

    state = {
        students: [],
        /*student: {
            StudentID: '',
            FirstName: '',
            LastName: '',
            MiddleInitial: '',
            Suffix: '',
            Nickname: '',
            SchoolType: '',
            SchoolName: '',
            SchoolDistrict: '',
            NextClass: '',
            ExpectedHighSchool: '',
            Address_Line1: '',
            Address_Line2: '',
            City: '',
            State: '',
            Zip: '',
            Birthdate: '',
            Gender: '',
            Ethnicity: '',
            PhoneNumber: '',
            Email: '',
            GraduationYear: '',
            Siblings: '',
            Gaurdian1: '',
            Gaurdian1Address_Line1: '',
            Gaurdian1Address_Line2: '',
            Gaurdian1Email: '',
            Gaurdian1Phone: '',
            Gaurdian2: '',
            Gaurdian2Address_Line1: '',
            Gaurdian2Address_Line2: '',
            Gaurdian2Email: '',
            Gaurdian2Phone: '',
            GT: '',
            EnglishLearner: '',
            NationalClearingHouse: '',
            YearAccepted: '',
            GradeAccepted: '',
            EnrollmentStatus: '',
            FundingStatus: '',
            FundingName: '',
            Mentor: '',
            Disability: '',
            Health: ''
        },*/
        pageVal: 0
    }

    componentDidMount() {
        this.getStudents();
    }

    getStudents = _ => {
        fetch('http://localhost:4000/students')
            .then(response => response.json())
            //.then(({ data }) => {console.log(data)})
            .then(response => this.setState({ students: response.data}))
            .catch(err => console.log(err))
    }

    addStudent = _ => {
        const { student } = this.state;
        fetch(`http://localhost:4000/students/add?ID=${student.ID}&FirstName=${student.FirstName}&MiddleName=${student.MiddleName}&LastName=${student.LastName}`)
            .then(response => response.json())
            .then(this.getStudents)
            .catch(err => console.error(err))
    }

    renderStudent = ({ ID, FirstName, MiddleName, LastName}) => <div key={ID}>{ID}, {FirstName}, {MiddleName}, {LastName}</div>

    render() {
        const { students, student } = this.state;
        return (
            <div className="App">
                {students.map(this.renderStudent)}

                <div>
                    <input
                        value={student.ID}
                        onChange={e => this.setState({ student: {...student, ID: e.target.value}})} />
                    <input
                        value={student.FirstName}
                        onChange={e => this.setState({ student: {...student, FirstName: e.target.value}})} />
                    <input
                        value={student.MiddleName}
                        onChange={e => this.setState({ student: {...student, MiddleName: e.target.value}})} />
                    <input
                        value={student.LastName}
                        onChange={e => this.setState({ student: {...student, LastName: e.target.value}})} />
                    <button onClick={this.addStudent}>Add Student</button>
                </div>
            </div>
        );
    }
}

export default App;
