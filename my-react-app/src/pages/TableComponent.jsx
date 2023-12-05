import React from 'react';

const TableComponent = ({ data }) => {
  // Assuming 'data' is an array of objects
  // The keys of the first object in the array will be used as table headers

  if (!data || data.length === 0) {
    return <p>No data available</p>;
  }

  const headers = Object.keys(data[0]);

  return (
    <table>
      <thead>
        <tr>
          {headers.filter((header,index) => header!="id").map((header, index) => (
            <th key={index}>{header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, rowIndex) => (
          <tr key={rowIndex}>
            {headers.filter((header,index) => header != "id").map((header, cellIndex) => (
              <td key={cellIndex}>{row[header]}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default TableComponent;
