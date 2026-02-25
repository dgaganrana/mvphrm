interface TableProps {
  headers: string[];
  rows: (string | number)[][];
}

export default function Table({ headers, rows }: TableProps) {
  return (
    <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "1rem" }}>
      <thead>
        <tr>
          {headers.map((h, i) => (
            <th key={i} style={{ borderBottom: "1px solid #ddd", padding: "0.5rem", textAlign: "left" }}>
              {h}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row, i) => (
          <tr key={i}>
            {row.map((cell, j) => (
              <td key={j} style={{ borderBottom: "1px solid #eee", padding: "0.5rem" }}>
                {cell}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
