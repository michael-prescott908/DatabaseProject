import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {

    state = {
        students: [],
        student: {
            ID: '',
            FirstName: '',
            MiddleName: '',
            LastName: ''
        },
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
