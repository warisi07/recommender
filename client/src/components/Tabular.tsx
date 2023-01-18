import Table from 'react-bootstrap/Table';
import { courses } from './courses';
import React, { useState } from 'react';

interface Props {
	currentItems: {
		'course number': string;
		'subject code': string;
		'course title': string;
	}[];
}

function Tabular(props: Props) {
	return props.currentItems.length === 1 ? (
		<p>
			Sorry, that search did not return any results! Please check your entry
			again
		</p>
	) : (
		<Table responsive striped bordered hover size='sm'>
			<thead>
				<tr>
					<th>Course number</th>
					<th>Department</th>
					<th>Name</th>
				</tr>
			</thead>
			<tbody>
				{/* Includes Temporary fix for error handling */}
				{props.currentItems.map((course) => {
					var courseLink =
						'https://classes.cornell.edu/browse/roster/SP23/class/' +
						course['subject code'] +
						'/' +
						course['course number'];

					return (
						<tr>
							<td>{course['course number']}</td>
							<td>{course['subject code']}</td>
							<td>
								<a href={courseLink} target='_blank'>
									{course['course title']}
								</a>
							</td>
						</tr>
					);
				})}
			</tbody>
		</Table>
	);
}

export default Tabular;
