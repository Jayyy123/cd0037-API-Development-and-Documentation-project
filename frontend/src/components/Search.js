import React, { Component } from 'react';

class Search extends Component {
  state = {
    query: '',
  };

  getInfo = (event) => {
    event.preventDefault();
    if(this.state.query !== ''){
      this.props.submitSearch(this.state.query);
    }else{
      alert('please type a search value')
    }
  };

  handleInputChange = () => {
    this.setState({
      query: this.search.value,
    });
  };

  render() {
    return (
      <form onSubmit={this.getInfo}>
        <input
          placeholder='Search questions...'
          ref={(input) => (this.search = input)}
          onChange={this.handleInputChange}
        />
        <input type='submit' value='Submit' className='button' />
      </form>
    );
  }
}

export default Search;
