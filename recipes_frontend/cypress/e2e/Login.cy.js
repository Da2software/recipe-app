describe('Login', () => {
    it('', () => {
      cy.visit('http://localhost:3000/login');
        cy.get('[id="username"]')
        .type('da2software');
        cy.get('[id="password"]')
        .type('Pass1234');
        cy.get('[id="btn-login"]')
        .click();
    });
});