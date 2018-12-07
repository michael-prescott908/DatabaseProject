import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import AddStudentPage from './AddStudentPage.js';

class App extends Component {

    state = {
        students: [],
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
        },
        pageVal: 0
    }



    getStudents = _ => {
        fetch('http://localhost:4000/students')
            .then(response => response.json())
            //.then(({ data }) => {console.log(data)})
            .then(response => this.setState({ students: response.data}))
            .catch(err => console.log(err))
    }

    AddStudentPage = () =>{
      this.setState({
        pageVal: 1
      });
    }

    goBack = () => {
      this.setState({
        pageVal: 0
      });
    }

    renderStudent = ({ ID, FirstName, MiddleName, LastName}) => <div key={ID}>{ID}, {FirstName}, {MiddleName}, {LastName}</div>

    render() {

        if(this.state.pageVal === 0){
        return (
            <div className="App" align="center">
                Welcome to the University for Young People!
                {console.log('I am running!')}
                <div>
                <button />
                    <button onClick={this.AddStudentPage}>Add Student</button>
                </div>
            </div>
        );
      }

      else if (this.state.pageVal === 1) {
        return (
            <div className="App">
                {console.log('I am running!')}
                <div>
                <button />
                    <AddStudentPage/>
                    <div align="left">
                      <button onClick={this.goBack}>Back</button>
                    </div>
                </div>
            </div>
          );
      }
    }
}

export default App;
