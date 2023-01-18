import React from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

function NavBar() {
	return (
		<Navbar bg='dark' variant='dark'>
			<Container>
				<Navbar.Brand href='/'>Course Recommender</Navbar.Brand>
			</Container>
		</Navbar>
	);
}

export default NavBar;
