describe('Home Page', () => {
  it('testing home page', () => {
    cy.visit('http://localhost:3000/')
    cy.get("h1").contains("Welcome")
    cy.get("h2").contains("The Seattle University TA Scheduler Application")

  
    cy.get("#survey-btn").contains("Survey").click()
    cy.location('pathname').should('eq', '/survey')
    cy.go('back')

    cy.get("#upload-btn").contains("Upload Course").click()
    cy.location('pathname').should('eq', '/upload-course')
    cy.go('back')

    cy.get("#assignment-btn").contains("Assignment").click()
    cy.location('pathname').should('eq', '/assignment-table')
    cy.go('back')

  })
})