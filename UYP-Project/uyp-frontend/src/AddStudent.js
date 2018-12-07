import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class AddStudentPage extends Component {

    state = {
        students: [],
        student: {
            StudentID: '',
            FirstName: '',
            LastName: '',
            MiddleInitial: '',
            Suffix: '',
            Nickname: '',
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
            Gaurdian1: '',
            GT: '',
            EnglishLearner: '',
            NationalClearingHouse: ''
        },
        pageVal: 0
    }

    addStudent = _ => {
        const { student } = this.state;
        fetch(`http://localhost:4000/students/add?ID=${student.ID}&FirstName=${student.FirstName}&MiddleName=${student.MiddleName}&LastName=${student.LastName}`)
            .then(response => response.json())
            .then(this.getStudents)
            .catch(err => console.error(err))
    }

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
                        value={student.LastName}
                        onChange={e => this.setState({ student: {...student, LastName: e.target.value}})} />
                    <input
                        value={student.MiddleInitial}
                        onChange={e => this.setState({ student: {...student, MiddleInitial: e.target.value}})} />

                    <input
                        value={student.Suffix}
                        onChange={e => this.setState({ student: {...student, Suffix: e.target.value}})} />
                    <input
                        value={student.Nickname}
                        onChange={e => this.setState({ student: {...student, Nickname: e.target.value}})} />
                    <input
                        value={student.Address_Line1}
                        onChange={e => this.setState({ student: {...student, Address_Line1: e.target.value}})} />
                    <input
                        value={student.Address_Line2}
                        onChange={e => this.setState({ student: {...student, Address_Line2: e.target.value}})} />
                    <input
                        value={student.City}
                        onChange={e => this.setState({ student: {...student, City: e.target.value}})} />


                    <input
                        value={student.State}
                        onChange={e => this.setState({ student: {...student, State: e.target.value}})} />
                    <input
                        value={student.Zip}
                        onChange={e => this.setState({ student: {...student, Zip: e.target.value}})} />
                    <input
                        value={student.Birthdate}
                        onChange={e => this.setState({ student: {...student, Birthdate: e.target.value}})} />
                    <input
                        value={student.Gender}
                        onChange={e => this.setState({ student: {...student, Gender: e.target.value}})} />
                    <input
                        value={student.Ethnicity}
                        onChange={e => this.setState({ student: {...student, Ethnicity: e.target.value}})} />


                    <input
                        value={student.PhoneNumber}
                        onChange={e => this.setState({ student: {...student, PhoneNumber: e.target.value}})} />
                    <input
                        value={student.Email}
                        onChange={e => this.setState({ student: {...student, Email: e.target.value}})} />
                    <input
                        value={student.GraduationYear}
                        onChange={e => this.setState({ student: {...student, GraduationYear: e.target.value}})} />
                    <input
                        value={student.GT}
                        onChange={e => this.setState({ student: {...student, GT: e.target.value}})} />
                    <input
                        value={student.Gaurdian1}
                        onChange={e => this.setState({ student: {...student, Gaurdian1: e.target.value}})} />



                    <button onClick={this.addStudent}>Add Student</button>
                </div>
            </div>
        );
    }
}

export default App;
