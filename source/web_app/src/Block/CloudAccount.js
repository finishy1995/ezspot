import React, { Component } from 'react';
import { withAuthenticator } from 'aws-amplify-react';
import EditableTable from '../Table/EditableTable';

class CloudAccount extends Component {
  columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      width: '15%',
      editable: true,
      type: 'text',
    }, {
      title: 'Type',
      dataIndex: 'type',
      width: '10%',
      editable: true,
      type: 'select',
      option: [
        'AWS Global',
        'AWS China'
      ],
    }, {
      title: 'Access key ID',
      dataIndex: 'ak',
      width: '20%',
      editable: true,
      type: 'text',
    }, {
      title: 'Secret access key',
      dataIndex: 'sk',
      width: '30%',
      editable: true,
      type: 'text',
    }
  ];
  state = {
    data: [
      {
        key: '0',
        name: 'test',
        type: 'AWS China',
        ak: 'AKIAJQUBSSQFH55VOOAA',
        sk: 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
      },
      {
        key: '1',
        name: 'test2',
        type: 'AWS China',
        ak: 'AKIAJQUBSSQFH55VOOAB',
        sk: 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
      }
    ]
  }
  
  save = (row, key) => {
    const newData = [...this.state.data];
    const index = newData.findIndex(item => key === item.key);
    
    if (index > -1) {
      const item = newData[index];
      newData.splice(index, 1, {
        ...item,
        ...row,
      });
      this.setState({ data: newData });
    } else {
      console.error(row, key);
    }
  }
  
  deleteItem = (key) => {
    const newData = [...this.state.data];
    newData.splice(key, 1);
    this.setState({ data: newData });
  }
  
  create = () => {
    const newData = [...this.state.data];
    newData.push({
      key: newData.length,
      name: '',
      type: 'AWS China',
      ak: '',
      sk: '',
    });
    this.setState({ data: newData });
  }
  
  render() {
    return (
      <div className="app-block">
        <h2>AWS Account</h2>
        <EditableTable
          columns={this.columns}
          data={this.state.data}
          save={this.save}
          deleteItem={this.deleteItem}
          create={this.create}
        />
      </div>
    );
  }
}

export default withAuthenticator(CloudAccount);
