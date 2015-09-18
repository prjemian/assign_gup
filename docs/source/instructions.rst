Instructions for the Review Panel Chairman
==========================================

.. rubric:: Outline

.. TODO: revise here

#. Before the proposal deadline

	#. Verify the members of the proposal review panel: `List of Reviewers`_
	#. Answer questions from review panel members.  CC the APS User Office.

#. After the proposal deadline

   #. `List of Proposals`_
   #. Run the ``Assign_GUP`` software.

      #. Create a new project file
      #. Import the proposals (from the XML file)
      #. Create the list of reviewers or Import from previous .agup file
      #. Edit reviewers to assign topic weights
      #. `Assign topic weights to each proposal`_
      #. `Assign Reviewers to Proposals`_
      #. `Update the Assignments on the Web site`_
      #. Prepare the boilerplate letter
      #. `Send emails`_

.. compound::

    .. _fig.main_window:

    .. figure:: resources/main_window.jpg
        :alt: fig.main_window
        :width: 60%

        Assign_GUP main window


List of Reviewers
~~~~~~~~~~~~~~~~~

.. sidebar:: At least a month before the GUP deadline...
   
   Check the reviewers and verify they all can attend on the review date.
   (GUP Calendar: http://www.aps.anl.gov/Users/Calendars/GUP_Calendar.htm)

#. Identify panel members whose terms expire soon.
#. Is a temporary reviewer necessary?
#. Identify new candidates to replace expiring panel members.
   Evaluate panel members strengths in the various topics for review
   and compare with proposal weights in each topic.  
   This will point out whether the panel has sufficient strength
   to review proposals on each topic.
#. Confirm the list of reviewers for the upcoming cycle.
#. Verify that each member can attend.
#. Assign values for reviewer strength on each topic.  
   Use a scale from 0 (no strength) to 1.0 (high strength), with 0.1 precision. 

.. compound::

    .. _fig.reviewers:

    .. figure:: resources/reviewers_editor.jpg
        :alt: fig.reviewers
        :width: 60%

        Editor: Reviewers

.. note:: In various example screen images shown in this documentation,
   the details of specific individuals or proposals has been removed
   or obscured to preserve anonymity.


List of Proposals
~~~~~~~~~~~~~~~~~

.. sidebar:: Be prompt! 

   Do this just after the proposal deadline.
   Assignments should be received within just a few days.
   Assigned reviewers must have sufficient to make their reviews.

#. Login to the Proposal review web site,
   (https://beam.aps.anl.gov/pls/apsweb/gup0008.panel_start_page?i_attrib=246B2411-PNL5),
   and click the "Download the list in XML" link.
   
     You might also consider using the "Print All Proposals" link
     to generate a single PDF file containing all the proposals and attachments.
     Any problem attachments will be noted on separate pages at the end of
     the document.
     Be sure to save that on-screen image to a file or it will go away 
     when you close your browser.
#. When that page appears, it will look unformatted and not like XML.  
   Don't worry, underneath the page is XML but is rendered poorly.
#. In your browser, choose "view source" (Control-U on Firefox)
   and save to a file such as ``raw-proposals-2015-2.xml`` (use the name of
   the proper review cycle).
#. This raw file may have characters that break the later XML processing.
   That's why I save it as raw and then make a working copy next.
#. Copy this file to ``proposals-2015-2.xml``
   and make one change first.  Add a ``period`` attribute (if not present) 
   to the root element ``Review_list`` with a value of the current 
   review cycle, such as::
   
     <Review_list period="2015-2">

Be on the lookout for:

* proposals that belong on another panel
* PUP or project proposals (they require additional reviewer work)
* identical or related proposals (may not be the same PI or beam line)
* ineligible reviewer(s) (ineligible since reviewer name is on the proposal)


List of Topics
~~~~~~~~~~~~~~

Central to this process is the creation of a list of topics.
These topics represent the various scientific or experimental
subjects represented by this suite of proposals.  Each of the
reviewers on the panel will have a different strength in each of
the topics.  This strength is represented as a decimal topic value, 
ranging between zero (no strength) to 1.0 (expert or confident).
The *dot product* of the topic values between any 
reviewer and proposal can be used as a measure of how appropriate
is that reviewer to evaluate that proposal. 

.. compound::

    .. _fig.topics:

    .. figure:: resources/topics_editor.jpg
        :alt: fig.topics
        :width: 40%

        Editor: topics

Initially, the list of topics is extracted from the proposals from the
list of subjects selected for each proposal by the proposal's author.

The list of topics may be edited to remove such nondescript names
as "Other" and to add in instrument-specific techniques such as XPCS
for which specific expertise may not be so common amongst the panel
reviewers.

Once the list of topics has been modified, check both the list of 
reviewers and the list of proposals that the topic values are
assigned properly.  (New topics added will be given topic values of 0.0.)


Assign topic weights to each proposal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Similar to the reviewers, each proposal must be assigned a topic weight.
The weight (a floating point decimal number) is the relevance of each topic to the proposal.
The scale is 0 to 1 where 0 means *not related* and 1 mean *related*.

When the proposals XML file is imported, a list of topics
is created from all the subjects as selected by the proposers.
Each topic created is assigned a weight of 1.0.  **These topic
assessments should be verified** since some proposers put down lots of
extraneous topics that are weakly related to the specifics of the proposal.


Assign Reviewers to Proposals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Choose a primary and a secondary reviewer for each proposal.
Most likely, these will be reviewers with the strongest topic weighting
for this proposal.  

.. compound::

    .. _fig.proposals:

    .. figure:: resources/proposals_editor.jpg
        :alt: fig.proposals
        :width: 60%

        Editor: Proposals

The rules are such that only one reviewer can be a *primary* and a 
different one can be *secondary*.

If a reviewer is ineligible to review a proposal (usually because they 
are named on the proposal team), their name will be grey and the
checkboxes to select them as either primary or secondary reviewer 
will be disabled.

Refer to the summary and analysis grid reports 
when attempting to balance the number of proposals assigned to 
each reviewer.


Update the Assignments on the Web site
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The assignments report gives a listing of the assigned reviewers 
for all proposals.  Looking at this page, enter the same information 
into the APS Review web site.  There is no upload capability 
possible for this data, you must enter it in from the web form.

.. compound::

    .. _fig.assignments:

    .. figure:: resources/assignments_report.jpg
        :alt: fig.assignments
        :width: 60%

        Report: Reviewer assignments


Send emails
~~~~~~~~~~~

Send emails to each reviewer listing the proposals on which they
are primary or secondary reviewer.  CC the APS User Office 
on each email.

To prepare the template for the emails, 
open the *Edit Email Template ...* from the *Editors* menu:

.. compound::

    .. _fig.substitution_keyword_editor:

    .. figure:: resources/substitution_keyword_editor.jpg
        :alt: fig.substitution_keyword_editor
        :width: 60%

        Editor: Email template and substitution keywords

To prepare the email text for each reviewer, select *Email Letters ...* from the 
*Reports* menu.  A new window will appear for each reviewer with details
specific to that reviewer.  Use this to create an email to each reviewer.
