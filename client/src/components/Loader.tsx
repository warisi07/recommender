import React from 'react';
import PulseLoader from 'react-spinners/PulseLoader';

interface Props {
	loading: boolean;
}

function Loader(props: Props) {
	return (
		<>
			<PulseLoader
				className='p-5'
				color='black'
				loading={props.loading}
				size={10}
				aria-label='Loading Spinner'
				data-testid='loader'
			/>
		</>
	);
}

export default Loader;
