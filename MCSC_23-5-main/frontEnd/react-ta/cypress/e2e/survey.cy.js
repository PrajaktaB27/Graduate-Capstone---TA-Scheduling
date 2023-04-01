describe('survey page', () => {
  it('checks survey page', () => {
    cy.visit('http://localhost:3000/survey')
    cy.get("h1").contains("Survey Page")
    cy.get(".box-main")

    cy.get("#instructor-start").contains("START INSTRUCTOR SURVEY").click()
    cy.location('pathname').should('eq', '/survey')
    cy.go('back')

    cy.visit('http://localhost:3000/survey')
    cy.get("#student-start").contains("START STUDENT SURVEY").click()
    //cy.location('pathname').should('eq', '/upload-course')
    cy.go('back')

    cy.visit('http://localhost:3000/survey')
    cy.get("#instructor-finish").contains("FINISH INSTRUCTOR SURVEY").click()
    //cy.location('pathname').should('eq', '/assignment-table')
    cy.go('back')

    cy.visit('http://localhost:3000/survey')
    cy.get("#student-finish").contains("FINISH STUDENT SURVEY").click()
    //cy.location('pathname').should('eq', '/assignment-table/assignment-table-history')
    cy.go('back')
  })
})