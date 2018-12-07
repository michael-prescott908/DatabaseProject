import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class AddStudentPage extends Component {

    state = {
      student: {
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
        Health: '',
        AcceptedSatte: 'Unaccepted'
      }
    }

    /*constructor(t_student){
      this.state.student = t_student;
    }*/

    addStudent = _ => {
        const { student } = this.state;
        fetch(`db.summersend.serverswc.com/students/add?ID=${this.state.student.ID}&FirstName=${this.state.student.FirstName}&LastName=${this.state.student.LastName}&MiddleInitial=${this.state.student.MiddleName}
              &Suffix=${this.state.student.Suffix}&Nickname=${this.state.student.Nickname}&SchoolType=${this.state.student.SchoolType}&SchoolName=${this.state.student.SchoolName}&SchoolDistrict=${this.state.student.SchoolDistrict}
              &NextClass=${this.state.student.NextClass}&ExpectedHighSchool=${this.state.student.ExpectedHighSchool}&Address_Line1=${this.state.student.Address_Line1}&Address_Line2=${this.state.student.Address_Line2}
              &City=${this.state.student.City}&State=${this.state.student.State}&Zip=${this.state.student.Zip}&Birthdate=${this.state.student.Birthdate}&Gender=${this.state.student.Gender}&Ethnicity=${this.state.student.Ethnicity}
              &PhoneNumber=${this.state.student.PhoneNumber}&Email=${this.state.student.Email}&GraduationYear=${this.state.student.GraduationYear}&Siblings=${this.state.student.Siblings}&Gaurdian1=${this.state.student.Gaurdian1}
              &Gaurdian1Address_Line1=${this.state.student.Gaurdian1Address_Line1}&Gaurdian1Address_Line2=${this.state.student.Gaurdian1Address_Line2}&Gaurdian1Email=${this.state.student.Gaurdian1Email}&Gaurdian1Phone=${this.state.student.Gaurdian1Phone}
              &Gaurdian2=${this.state.student.Gaurdian2}&Gaurdian2Address_Line1=${this.state.student.Gaurdian2Address_Line1}&Gaurdian2Address_Line2=${this.state.student.Gaurdian2Address_Line2}&Gaurdian2Email=${this.state.student.Gaurdian2Email}
              &Gaurdian2Phone=${this.state.student.Gaurdian2Phone}&GT=${this.state.student.GT}`)
            .then(response => response.json())
            .then(this.getStudents)
            .catch(err => console.error(err))
    }

    goBack = () => {

    }

    render() {
        const { student } = this.state;
        return (
            <div className="AddStudentPage">
                <div align="center">
                    Welcome to the UYP application! <br/>
                    Please fill out the required information!<br/><br/><br/>
                    <div align="left">
                        Student First Name:{" "}
                        <input
                            value={student.FirstName}
                            onChange={e => this.setState({ student: {...student, FirstName: e.target.value}})} />
                            <br/>

                        Student Last Name:{" "}
                        <input
                            value={student.LastName}
                            onChange={e => this.setState({ student: {...student, LastName: e.target.value}})} />
                            <br/>

                        Student Middle Initial:{" "}
                        <input
                            value={student.MiddleInitial}
                            onChange={e => this.setState({ student: {...student, MiddleInitial: e.target.value}})} />
                            <br/>

                        Student Suffix:{" "}
                        <input
                            value={student.Suffix}
                            onChange={e => this.setState({ student: {...student, Suffix: e.target.value}})} />
                            <br/>

                        Student Preferred Name:{" "}
                        <input
                            value={student.Nickname}
                            onChange={e => this.setState({ student: {...student, Nickname: e.target.value}})} />
                            <br/>

                        Address Line 1:{" "}
                        <input
                            value={student.Address_Line1}
                            onChange={e => this.setState({ student: {...student, Address_Line1: e.target.value}})} />
                            <br/>

                        Address Line 2:{" "}
                        <input
                            value={student.Address_Line2}
                            onChange={e => this.setState({ student: {...student, Address_Line2: e.target.value}})} />
                            <br/>

                        City:{" "}
                        <input
                            value={student.City}
                            onChange={e => this.setState({ student: {...student, City: e.target.value}})} />
                            <br/>

                        State:{" "}
                        <input
                            value={student.State}
                            onChange={e => this.setState({ student: {...student, State: e.target.value}})} />
                            <br/>

                        Zip:{" "}
                        <input
                            value={student.Zip}
                            onChange={e => this.setState({ student: {...student, Zip: e.target.value}})} />
                            <br/>

                        Birthdate:{" "}
                        <input
                            value={student.Birthdate}
                            onChange={e => this.setState({ student: {...student, Birthdate: e.target.value}})} />
                            <br/>

                        Gender:{" "}
                        <input
                            value={student.Gender}
                            onChange={e => this.setState({ student: {...student, Gender: e.target.value}})} />
                            <br/>

                        Ethnicity:{" "}
                        <input
                            value={student.Ethnicity}
                            onChange={e => this.setState({ student: {...student, Ethnicity: e.target.value}})} />
                            <br/>

                        Type of School:{" "}
                        <input
                            value={student.SchoolType}
                            onChange={e => this.setState({ student: {...student, SchoolType: e.target.value}})} />
                            <br/>

                        Name of School:{" "}
                        <input
                            value={student.SchoolName}
                            onChange={e => this.setState({ student: {...student, SchoolName: e.target.value}})} />
                            <br/>

                        School District:{" "}
                        <input
                            value={student.SchoolDistrict}
                            onChange={e => this.setState({ student: {...student, SchoolDistrict: e.target.value}})} />
                            <br/>

                        Upcoming Grade:{" "}
                        <input
                            value={student.NextClass}
                            onChange={e => this.setState({ student: {...student, NextClass: e.target.value}})} />
                            <br/>

                        Graduation Year:{" "}
                        <input
                            value={student.GraduationYear}
                            onChange={e => this.setState({ student: {...student, GraduationYear: e.target.value}})} />
                            <br/>

                        Email:{" "}
                        <input
                            value={student.Email}
                            onChange={e => this.setState({ student: {...student, Email: e.target.value}})} />
                            <br/>

                        Phone Number:{" "}
                        <input
                            value={student.PhoneNumber}
                            onChange={e => this.setState({ student: {...student, PhoneNumber: e.target.value}})} />
                            <br/>

                        Gifted and Talented?:{" "}
                        <input
                            value={student.GT}
                            onChange={e => this.setState({ student: {...student, GT: e.target.value}})} />
                            <br/>

                        Gaurdian #1 name: {" "}
                        <input
                            value={student.Gaurdian1}
                            onChange={e => this.setState({ student: {...student, Gaurdian1: e.target.value}})} />
                            <br/>

                        Gaurdian #1 Address Line 1: {" "}
                        <input
                            value={student.Gaurdian1Address_Line1}
                            onChange={e => this.setState({ student: {...student, Gaurdian1Address_Line1: e.target.value}})} />
                            <br/>

                        Gaurdian #1 Address Line 2: {" "}
                        <input
                            value={student.Gaurdian1Address_Line2}
                            onChange={e => this.setState({ student: {...student, Gaurdian1Address_Line2: e.target.value}})} />
                            <br/>

                        Gaurdian #1 Email: {" "}
                        <input
                            value={student.Gaurdian1Email}
                            onChange={e => this.setState({ student: {...student, Gaurdian1Email: e.target.value}})} />
                            <br/>

                        Gaurdian #1 Phone Number: {" "}
                        <input
                            value={student.Gaurdian1Phone}
                            onChange={e => this.setState({ student: {...student, Gaurdian1Phone: e.target.value}})} />
                            <br/>

                        Gaurdian #2 name: {" "}
                        <input
                            value={student.Gaurdian2}
                            onChange={e => this.setState({ student: {...student, Gaurdian2: e.target.value}})} />
                            <br/>

                        Gaurdian #2 Address Line 1: {" "}
                        <input
                            value={student.Gaurdian2Address_Line1}
                            onChange={e => this.setState({ student: {...student, Gaurdian2Address_Line1: e.target.value}})} />
                            <br/>

                        Gaurdian #2 Address Line 2: {" "}
                        <input
                            value={student.Gaurdian2Address_Line2}
                            onChange={e => this.setState({ student: {...student, Gaurdian2Address_Line2: e.target.value}})} />
                            <br/>

                        Gaurdian #2 Email: {" "}
                        <input
                            value={student.Gaurdian2Email}
                            onChange={e => this.setState({ student: {...student, Gaurdian2Email: e.target.value}})} />
                            <br/>

                        Gaurdian #2 Phone Number: {" "}
                        <input
                            value={student.Gaurdian2Phone}
                            onChange={e => this.setState({ student: {...student, Gaurdian2Phone: e.target.value}})} />
                            <br/>

                            <button onClick={this.addStudent}>Add Student</button>
                            <br/>
                    </div>
                </div>
            </div>
        );
    }
}

export default AddStudentPage;
