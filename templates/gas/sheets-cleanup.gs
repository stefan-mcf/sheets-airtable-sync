function normalizeRowsFixtureOnly() {
  // Fixture sample: trim strings before exporting to the local sync proof.
  const sheet = SpreadsheetApp.getActiveSheet();
  const range = sheet.getDataRange();
  const values = range.getValues().map(row => row.map(cell => typeof cell === 'string' ? cell.trim() : cell));
  range.setValues(values);
}
