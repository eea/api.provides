""" Base test cases
"""
from Products.CMFPlone import setuphandlers
from plone.testing import z2
from plone.app.testing import TEST_USER_ID
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import setRoles


class EEAFixture(PloneSandboxLayer):
    """ EEA Testing Policy
    """
    def setUpZope(self, app, configurationContext):
        """ Setup Zope
        """
        import plone.restapi
        import eea.api.objectprovides
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=eea.api.objectprovides)
        z2.installProduct(app, 'eea.api.objectprovides')

    def setUpPloneSite(self, portal):
        """ Setup Plone
        """
        applyProfile(portal, 'eea.api.objectprovides:default')

        # Default workflow
        wftool = portal['portal_workflow']
        wftool.setDefaultChain('simple_publication_workflow')

        # Login as manager
        setRoles(portal, TEST_USER_ID, ['Manager'])

        # Add default Plone content
        try:
            applyProfile(portal, 'plone.app.contenttypes:plone-content')
        except KeyError:
            # BBB Plone 4
            setuphandlers.setupPortalContent(portal)

        # Create testing environment
        portal.invokeFactory("Folder", "sandbox", title="Sandbox")


    def tearDownZope(self, app):
        """ Uninstall Zope
        """
        z2.uninstallProduct(app, 'eea.api.objectprovides')

EEAFIXTURE = EEAFixture()
FUNCTIONAL_TESTING = FunctionalTesting(bases=(EEAFIXTURE,),
                                       name='EeaApiObjectprovides:Functional')
