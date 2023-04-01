import React from 'react'
import ErrorPage from './ErrorPage'

describe('<ErrorPage />', () => {
  it('Default Message', () => {
    // see: https://on.cypress.io/mounting-react
    cy.mount(<ErrorPage />)
    cy.get('#message').should('have.text','ERROR 404 PAGE NOT FOUND')
  })
})