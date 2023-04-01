describe('Nav Bar', () => {

  it('click all links', () => {

    cy.visit('http://localhost:3000/')
  
    // home page
    cy.contains('Home').click()
    cy.location('pathname').should('eq', '/')
    cy.go('back')

    // Survey page
    cy.contains('Survey').click()
    cy.location('pathname').should('eq', '/survey')
    cy.go('back')

    // Upload Course page
    cy.contains('Upload Course').click()
    cy.location('pathname').should('eq', '/upload-course')
    cy.go('back')

    // Assignment Table page
    cy.contains('Assignment Table').click()
    cy.location('pathname').should('eq', '/assignment-table')
    cy.go('back')

    // History page
    cy.contains('History').click()
    cy.location('pathname').should('eq', '/assignment-table/assignment-table-history')
    cy.go('back')

    // Instructor page
    cy.contains('Instructor').click()
    cy.location('pathname').should('eq', '/instructor')
    cy.go('back')

    // Student Worker page
    cy.contains('Student Worker').click()
    cy.location('pathname').should('eq', '/student-worker')
    cy.go('back')

     
   

  });
  
})