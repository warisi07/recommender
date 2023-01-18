import React from 'react';

interface Props {
	submitFormDataFromTitle: (
		e: React.FormEvent,
		data: {
			courseId: string;
			queryNumber: string;
		}
	) => Promise<void>;

	submitFormDataFromKeyword: (
		e: React.FormEvent,
		data: {
			keyword: string;
			number: string;
		}
	) => Promise<void>;
}

function Hero(props: Props) {
	// const [courseIdFromTitle, setCourseIdFromTitle] = React.useState('');
	// const [courseNumberFromTitle, setCourseNumberFromTitle] = React.useState('');

	const [courseIdFromKeyword, setCourseIdFromKeyword] = React.useState('');
	const [courseNumberFromKeyword, setCourseNumberFromKeyword] =
		React.useState('');

	// const submitFormTitle = (e: React.FormEvent<HTMLFormElement>) => {
	// 	e.preventDefault();
	// 	const data = {
	// 		courseId: courseIdFromTitle,
	// 		queryNumber: '150',
	// 	};

	// 	return props.submitFormDataFromTitle(e, data);
	// };

	const submitFormKeyword = (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		const data = {
			keyword: courseIdFromKeyword,
			number: '200',
		};

		return props.submitFormDataFromKeyword(e, data);
	};

	return (
		<div className='container body-content fw-light mt-5'>
			<p>
				This is a fun experiment to see if we can improve course search at
				Cornell
			</p>
			<p>
				<strong>Background</strong>: This search uses a machine learning model
				that has been trained on the course descriptions of all courses in SP23
				scraped from <a href='https://classes.cornell.edu'>here</a>
			</p>
			<p>
				Enter keywords below to predict up to 200 courses you might like. Enter
				sentences if you wish. Describe what you're looking for in a course and
				see if the model can be of any help. If you don't get any results back,
				please check you're spelling things correctly, or rephrase your query.
			</p>
			<p>Feedback? Shoot me an email here - ascents.slicer.0d@icloud.com</p>
			<hr />
			{/* <form
				className='row g-3'
				onSubmit={(e: React.FormEvent<HTMLFormElement>) => submitFormTitle(e)}>
				<div className='col-auto'>
					<input
						value={courseIdFromTitle}
						type='text'
						className='form-control'
						placeholder='Course name'
						onChange={(e) => setCourseIdFromTitle(e.target.value)}
					/>
				</div> */}
			{/* <div className='col-auto'>
					<input
						value={courseNumberFromTitle}
						type='number'
						className='form-control'
						placeholder='Query number'
						onChange={(e) => setCourseNumberFromTitle(e.target.value)}
					/>
				</div> */}
			{/* <div className='col-auto'>
					<button type='submit' className='btn btn-primary mb-2'>
						Search Courses
					</button>
				</div>
			</form> */}

			{/* <div>OR</div> */}
			<form className='row g-3 mt-1' onSubmit={submitFormKeyword}>
				<div className='col-auto'>
					<input
						value={courseIdFromKeyword}
						required
						type='text'
						className='form-control'
						placeholder='Keywords'
						onChange={(e) => setCourseIdFromKeyword(e.target.value)}></input>
				</div>
				{/* <div className='col-auto'>
					<input
						type='number'
						value={courseNumberFromKeyword}
						className='form-control'
						placeholder='query number'
						onChange={(e) => setCourseNumberFromKeyword(e.target.value)}
					/>
				</div> */}
				<div className='col-auto'>
					<button type='submit' className='btn btn-primary mb-3'>
						Search Courses
					</button>
				</div>
			</form>
		</div>
	);
}

export default Hero;
