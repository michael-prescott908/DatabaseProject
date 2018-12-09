import React from 'react';
import { HashRouter, Route } from 'react-router-dom';

// Pages
import HomePage from './HomePage.js';

class App extends React.Component {
	render() {
		return (
			<HashRouter>
				<div>
					{ console.log(`I'm here`) }
					<Route exact path="/" component={HomePage} />
				</div>
			</HashRouter>
		);
	}
}

export default App;
