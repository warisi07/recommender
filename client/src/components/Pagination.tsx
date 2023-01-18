import React from 'react';
import ReactPaginate from 'react-paginate';
import Tabular from './Tabular';

interface Props {
	itemsPerPage: number;
	content: {
		'subject code': string;
		'course number': string;
		'course title': string;
	}[];
	forcePage: number;
}

function Pagination(props: Props) {
	const [currentItems, setCurrentItems] = React.useState([
		{ 'subject code': '', 'course number': '', 'course title': '' },
	]);
	const [pageCount, setPageCount] = React.useState(0);

	const [itemsOffset, setItemOffset] = React.useState(0);
	const [page, setPage] = React.useState(0);

	React.useEffect(() => {
		const endOffSet = itemsOffset + props.itemsPerPage;
		setCurrentItems(props.content.slice(itemsOffset, endOffSet));
		setPageCount(Math.ceil(props.content.length / props.itemsPerPage));
	}, [itemsOffset, props.content, props.itemsPerPage, page]);

	const handlePageClick = (e: any) => {
		const newOffSet = (e.selected * props.itemsPerPage) % props.content.length;
		setItemOffset(newOffSet);
		window.scrollTo(0, 0);
	};

	return (
		<>
			<div className='container align-items-center d-flex justify-content-center mt-5'>
				<Tabular currentItems={currentItems} />
			</div>
			{/* Pagination coming soon? */}
			{/* <ReactPaginate
				breakLabel='...'
				nextLabel='next'
				breakClassName='page-item'
				breakLinkClassName='page-link'
				containerClassName='pagination justify-content-center'
				pageClassName='page-item'
				pageLinkClassName='page-link'
				previousClassName='page-item'
				previousLinkClassName='page-link'
				nextClassName='page-item'
				nextLinkClassName='page-link'
				activeClassName='active'
				forcePage={props.forcePage}
				onPageChange={handlePageClick}
				pageRangeDisplayed={5}
				pageCount={pageCount}
				previousLabel='previous'
				renderOnZeroPageCount={undefined}
			/> */}
		</>
	);
}

export default Pagination;
