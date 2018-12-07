import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class ViewClassesPage extends Component {

    state = {
        classes: [],
        class: {
          CourseID: '',
          Course_Name: '',
          Department: ''
        }
    }

    componentDidMount() {
        this.getClasses();
    }

    getClasses = _ => {
        fetch('db.summersend.serverswc.com/classes')
            .then(response => response.json())
            //.then(({ data }) => {console.log(data)})
            .then(response => this.setState({ classes: response.data}))
            .catch(err => console.log(err))
    }

    renderClass = ({ CourseID, Course_Name, Department}) => <div key={CourseID}>{CourseID}| {Course_Name}| {Department}</div>

    render() {
      const { classes, class_i } = this.state;
      return(
        <div className="ViewClassesPage">
          {classes.map(this.renderClass)}
        </div>
      );
    }
}

export default ViewClassesPage;
