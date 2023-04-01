 import React, { Component } from 'react';
 
 class Test extends Component {
    state = { 
        count: 0
    };
    
    // constructor() {
    //     super();
    //     this.handleIncrement = this.handleIncrement.bind(this);
    // }
    
    handleIncrement =(product) => {
        console.log(product);
        this.setState({ count: this.state.count + 1 });
    }

    render() { 
        return 
            <div>
                <h1>Hello World</h1>
                <><button onClick={() => this.handleIncrement(product)}>Click me</button></>
            </div>;
    }
 }
  
 export default Test;