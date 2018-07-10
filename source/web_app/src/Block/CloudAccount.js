import React, { Component } from 'react';
import { message } from 'antd';
import EditableTable from '../Table/EditableTable';
import { call } from '../Tool/API';

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
    data: [],
    loading: true
  }
  
  constructor(props) {
    super(props);
    var caller = this;
    
    call('get', '/account', {}, function (error, data) {
      var new_data = [];
      for (var i=0; i<data.length; i++)
        new_data.push({
          key: data[i]['account_id'],
          name: data[i]['account_name'],
          type: data[i]['account_type'],
          ak: data[i]['ak'],
          sk: data[i]['sk_show'],
        });
        
      caller.setState({ data: new_data, loading: false });
    });
  }
  
  save = (row, key) => {
    console.log(row);
    const newData = [...this.state.data];
    const index = newData.findIndex(item => key === item.key);
    
    if (index > -1) {
      const item = newData[index];
      newData.splice(index, 1, {
        ...item,
        ...row,
      });
      this.setState({ data: newData });
      
      if ((newData[index]['key'].length < 12) && (newData[index]['key'].slice(0,4) === 'tmp:')) {
        call('post', '/account', {
          'accounts': [{
            'account_name': newData[index]['name'],
            'account_type': newData[index]['type'],
            'ak': newData[index]['ak'],
            'sk': newData[index]['sk'],
          }]
        }, function (error, data) {
          if (error) {
            console.error(error);
            message.error('Account create failed.');
          } else
            message.success('Account create succeeded.');
        });
      } else {
        var account = {
          'account_id': newData[index]['key'],
          'account_name': newData[index]['name'],
          'account_type': newData[index]['type'],
          'ak': newData[index]['ak'],
        };
        if (newData[index]['sk'].indexOf('****')<=-1)
          account['sk'] = newData[index]['sk'];
        
        call('put', '/account', {
          'accounts': [account]
        }, function (error, data) {
          if (error) {
            console.error(error);
            message.error('Account update failed.');
          } else
            message.success('Account update succeeded.');
        });
      }
    } else {
      console.error(row, key);
    }
  }
  
  deleteItem = (key) => {
    const newData = [...this.state.data];
    const index = newData.findIndex(item => key === item.key);
    
    call('delete', '/account', {
      'accounts': [{
        'account_id': newData[index]['key']
      }]
    }, function (error, data) {
      if (error) {
        console.error(error);
        message.error('Account delete failed.');
      } else
        message.success('Account create succeeded.');
    });
    newData.splice(index, 1);
    this.setState({ data: newData });
  }
  
  create = () => {
    const newData = [...this.state.data];
    newData.push({
      key: 'tmp:'+newData.length,
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
          loading={this.state.loading}
        />
      </div>
    );
  }
}

export default CloudAccount;
