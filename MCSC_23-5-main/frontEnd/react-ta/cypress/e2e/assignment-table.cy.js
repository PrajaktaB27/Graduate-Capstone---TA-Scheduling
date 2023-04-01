describe('assignment page', () => {
  it('checks assignment page', () => {
    cy.visit('http://localhost:3000/assignment-table')
    cy.get(".AssignmentTable")
    cy.get(".QuarterID")
    cy.get("h1").contains("Assignment Table for Winter Quarter 2023")
    


  })
})