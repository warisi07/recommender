import { useState } from 'react';
import reactLogo from './assets/react.svg';
import './App.css';
import NavBar from './components/NavBar';
import Hero from './components/Hero';
import { courses } from './components/courses';
import Pagination from './components/Pagination';
import Loader from './components/Loader';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BASE_URL } from './constants';
import React from 'react';

function App() {
	const [loading, setLoading] = React.useState(false);
	const [course, setCourse] = React.useState();
	const [page, setPage] = React.useState(1);

	const [loadingText, setLoadingText] = React.useState(
		'Loading courses...this might take a minute'
	);

	function generateLoadingText() {
		if (loading) {
			setTimeout(() => {
				if (loading) {
					setLoadingText('Hold on...any second now');
				}
			}, 10000);
			return <p className='m-0'>{loadingText}</p>;
		}
	}

	const getCoursesSearchByTitle = async (
		e: React.FormEvent,
		data: {
			courseId: string;
			queryNumber: string;
		}
	): Promise<void> => {
		setLoading(true);
		try {
			const response = await fetch(BASE_URL + '/title', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(data),
			});
			const result = await response.json();
			setCourse(result);
			setLoading(false);
			setPage(1);
		} catch (err) {
			console.log(err);
		}
	};

	const getCoursesSearchByKeyword = async (
		e: React.FormEvent,
		data: {
			keyword: string;
			number: string;
		}
	): Promise<void> => {
		setLoading(true);
		try {
			const response = await fetch(BASE_URL + '/keyword', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(data),
			});
			const result = await response.json();
			setCourse(result);
			setLoading(false);
		} catch (err) {
			console.log(err);
		}
	};

	return (
		<div>
			<NavBar />
			<Hero
				submitFormDataFromTitle={getCoursesSearchByTitle}
				submitFormDataFromKeyword={getCoursesSearchByKeyword}
			/>
			{course && (
				<Pagination itemsPerPage={200} content={course} forcePage={page} />
			)}

			{loading && (
				<div className='container align-items-center d-flex justify-content-center text-center'>
					<div>
						<Loader loading={loading} />
						{generateLoadingText()}
					</div>
				</div>
			)}

			{/* <footer className='footer mt-auto py-3 bg-light'>
				<div className='container'>
					<span className='text-muted'>Made with ❤️ by </span>
					<a href='https://github.com/akinfelami/class-recommender'>
						Akinfolami Akin-Alamu{'   '}
					</a>
				</div>
			</footer> */}
		</div>
	);
}

export default App;
