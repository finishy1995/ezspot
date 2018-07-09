import React, { Component } from 'react';
import { Table, Input, InputNumber, Popconfirm, Form, Select, Divider, Button } from 'antd';
import './Table.css';

const FormItem = Form.Item;
const EditableContext = React.createContext();
const Option = Select.Option;

const EditableRow = ({ form, index, ...props }) => (
  <EditableContext.Provider value={form}>
    <tr {...props} />
  </EditableContext.Provider>
);
const EditableFormRow = Form.create()(EditableRow);

class EditableCell extends Component {
  getInput = () => {
    if (this.props.inputType === 'number') {
      return <InputNumber />;
    }
    if (this.props.inputType === 'select') {
      return (
        <Select initialValue={ this.props.inputOption[0] }>
          { this.props.inputOption.map((option) => {
            return (
              <Option value={ option } key={ option }>{ option }</Option>
            );
          }) }
        </Select>
      );
    }
    return <Input />;
  };

  render() {
    const {
      editing,
      dataIndex,
      index,
      inputType,
      inputOption,
      validator,
      title,
      record,
      ...restProps
    } = this.props;
    
    return (
      <EditableContext.Consumer>
        {(form) => {
          const { getFieldDecorator } = form;
          return (
            <td {...restProps}>
              {editing ? (
                <FormItem style={{ margin: 0 }}>
                  {getFieldDecorator(dataIndex, {
                    rules: [{
                      required: true,
                      message: `Please Input ${title}!`,
                    }],
                    initialValue: record[dataIndex],
                  })(this.getInput())}
                </FormItem>
              ) : restProps.children}
            </td>
          );
        }}
      </EditableContext.Consumer>
    );
  }
}

class EditableTable extends Component {
  state = {
    editingKey: ''
  };

  constructor(props) {
    super(props);
    this.columns = this.getColumns();
  }

  isEditing = (record) => {
    return record.key === this.state.editingKey;
  };

  edit(key) {
    this.setState({ editingKey: key });
  }

  deleteItem(key) {
    this.setState({ editingKey: '' });
    this.props.deleteItem(key);
  }

  create = () => {
    this.setState({ editingKey: this.props.data.length });
    this.props.create();
  }

  cancel = (key) => {
    this.setState({ editingKey: '' });
  };
  
  save(form, key) {
    form.validateFields((error, row) => {
      if (error) return;
      
     this.setState({ editingKey: '' });
     this.props.save(row, key);
    });
  }

  getColumns() {
    var columns = this.props.columns;
    columns.push({
      title: 'operation',
      render: (text, record) => {
        const editable = this.isEditing(record);
        return (
          <div>
            {editable ? (
              <span>
                <EditableContext.Consumer>
                  {form => (
                    <a
                      onClick={() => this.save(form, record.key)}
                      style={{ marginRight: 8 }}
                    >
                      Save
                    </a>
                  )}
                </EditableContext.Consumer>
                <Popconfirm
                  title="Sure to cancel?"
                  onConfirm={() => this.cancel(record.key)}
                >
                  <a>Cancel</a>
                </Popconfirm>
              </span>
            ) : (
              <a onClick={() => this.edit(record.key)}>Edit</a>
            )}
            <Divider type="vertical" />
            <a onClick={() => this.deleteItem(record.key)}>Delete</a>
          </div>
        );
      },
    });
    
    return columns.map((col) => {
      if (!col.editable) {
        return col;
      }
      
      return {
        ...col,
        onCell: record => ({
          record,
          inputType: col.type,
          dataIndex: col.dataIndex,
          title: col.title,
          inputOption: col.option,
          validator: col.validator,
          editing: this.isEditing(record),
        }),
      };
    });
  }

  render() {
    const components = {
      body: {
        row: EditableFormRow,
        cell: EditableCell,
      },
    };

    return (
      <div>
        <div className="table-operations">
          <Button type="primary" onClick={ this.create }>Create</Button>
        </div>
        <Table
          components={components}
          bordered
          dataSource={this.props.data}
          columns={this.columns}
          rowClassName="editable-row"
        />
      </div>
    );
  }
}

export default EditableTable;
