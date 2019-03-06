.. title: How To Give A PyCon Presentation
.. slug: presentation-advice
.. date: 2018-05-12 10:22:54 UTC+07:00
.. tags:
.. category:
.. link:
.. description:
.. type: text


How To Give A PyCon Presentation is based on a document by Prof. `Michael Ernst`_ . Used with permission. Original at https://homes.cs.washington.edu/~mernst/advice/giving-talk.html

.. _Michael Ernst: https://homes.cs.washington.edu/~mernst/


Introduction
=============

There are many good references regarding how to give an effective talk — that is, a technical presentation, whether at a conference,
to your research group, or as an invited speaker at another university or research laboratory.
This page cannot replace them, but it does briefly note a few issyra very frequently seen in talks.

Get feedback by giving a practice talk! One of the most effective ways to improve your work is to see the reactions
of others and get their ideas and advice.

Think about the presentations you attend (or have attended in the past), especially if they are similar in some way to yours. What was boring about the other presentations? What was interesting about them? What did you take away from the presentation? What could you have told someone about the topic, 30 minutes after the end of the presentation?

The content
============

Before you start preparing a talk, you need to know your goal and know your audience.
You will have to customize your presentation to its purpose. Even if you have previously created a talk for another venue, you may have to make a new one, particularly if you have done more work in the meanwhile.

The goal of a talk at PyCon is to engage the audience. You have found something interresting or developped some software, and you need to convince the audience of 3 things: there is an interesting  problem (it is a real problem, and a solution would be useful), the problem is hard (not already solved, or existing solutions have issues), and that you have found a (better) solution to it. If any of these three pieces is missing, your talk is much less likely to be a success. So be sure to provide motivation for your work, provide background about the problem, and supply sufficient technical details.

When you give a talk, ask yourself, “What are the key points that my audience should take away from the talk?” Then, elide everything that does not support those points. If you try to say too much (a tempting mistake), then your main points won't strike home and you will have wasted everyone's time. In particular, do not try to include all the details about the tools/software you are presenting. Avoid live coding/demo, they have an uncanny tendency to fail.

A good way to determine what your talk should say is to explain your ideas verbally to someone who does not already understand them. Do this before you have tried to create slides (you may use a blank whiteboard, but that often is not necessary). You may need to do this a few times before you find the most effective way to present your material. Notice what points you made and in what order, and organize the talk around that. Slides should not be a crutch that constrains you talk, but they should support the talk you want to give.

Do not try to fit too much material in a talk. About one slide per minute is a good pace (if lots of your slides are animations that take only moments to present, you can have more slides). Remember what your key points are, and focus on those. Don't present more information than your audience can grasp; for example, often intuitions and an explanation of the approach are more valuable than the gory details of an implementation. If you try to explain all the details into a talk, you will rush, with the result that the audience may come away understanding nothing. It's better to think of the talk as an advertisement for the software that gives the key ideas, intuitions, and results, and that makes the audience eager to explore the software/library or to talk with you to learn more. That does not mean holding back important details — merely omitting less important ones. You may also find yourself omitting entire portions that do not directly contribute to the main point you are trying to make in your talk.

Just as there should be no extra slides, there should be no missing slides. As a rule, you shouldn't speak for more than a minute or so without having new information appear. If you have an important point to make, then have a slide to support it. (Very few people can mesmerize an audience on a technical topic, and leave the audience with a deep understanding of the key points, without any visual props. Unfortunately, you are probably not one of them, at least not yet.) As a particularly egregious example, do not discuss a user interface without presenting a picture of it — perhaps multiple ones. As another example, you should not dwell on the title slide for very long, but should present a picture relevant to the problem you are addressing, to make the motivation for your work concrete.

The slides
===========

Slide titles
-------------

Use descriptive slide titles. Do not use the same title on multiple slides (except perhaps when the slides constitute an animation or build). Choose a descriptive title that helps the audience to appreciate what the specific contribution of this slide is. If you can't figure that out, it suggests that you have not done a good job of understanding and organizing your own material.

Introduction
-------------

Start your talk with motivation and examples — and have lots of motivation and examples throughout. For the very beginning of your talk, you need to convince the audience that this talk is worth paying attention to: it is solving an important and comprehensible problem. Your first slide should be an example of the problem you are solving, or some other motivation.

Outline slides
---------------

Never start your talk with an outline slide. (That's boring, and it's too early for the audience to understand the talk structure yet.) Outline slides can be useful, especially in a talk that runs longer than 30 minutes, because they helps the audience to regain its bearings and to keep in mind your argument structure. Present an outline slide (with the current current section indicated via color, font, and/or an arrow) at the beginning of each major section of the talk, other than the introductory, motivational section.

Conclusion
--------------

The last slide should be a contributions or conclusions slide, reminding the audience of the take-home message of the talk. Do not end the talk with future work, or with a slide that says “questions” or “thank you” or “the end” or merely gives your email address. And, leave your contributions slide up after you finish the talk (while you are answering questions). One way to think about this rule is: What do you want to be the last thing that the audience sees (or that it sees while you field questions)?

Builds
-------

When a subsequent slide adds material to a previous one (or in some other way just slightly changes the previous slide; this is sometimes called a “build”), all common elements must remain in exactly the same position. A good way to check this is to quickly transition back and forth between the two slides several times. If you see any jitter, then correct the slide layout to remove it. You may need to leave extra space on an early slide to accommodate text or figures to be inserted later; even though that space may look a little unnatural, it is better than the alternative. If there is any jitter, the audience will know that something is different, but will be uneasy about exactly what has changed (the human eye is good at detecting the change but only good at localizing changes when those changes are small and the changes are smooth). You want the audience to have confidence that most parts of the slide have not changed, and the only effective way to do that is not to change those parts whatsoever. You should also consider emphasizing (say, with color or highlighting) what has been added on each slide.

Keep slides uncluttered
------------------------

Don't put too much text (or other material) on a slide. When a new slide goes up, the audience will turn its attention to comprehending that slide. If the audience has to read a lot of text, they will tune you out, probably missing something important. This is one reason the diagrams must be simple and clear, and the text must be telegraphic. As a rule of thumb, 3 lines of text for a bullet point is always too much, and 2 full lines is usually too much. Shorten the text, or break it into pieces (say, subbullet points) so that the audience can skim it without having to ignore you for too long.


When presenting the slides
---------------------------

Do not read your slides word-for-word. Reading your slides verbatim is very boring and will cause the audience to tune out. You are also guaranteed to go too fast for some audience members and too slow for others, compared to their natural reading speed, thus irritating many people. If you find yourself reading your slides, then there is probably too much text on your slides. The slides should be an outline, not a transcript. That is, your slides should give just the main points, and you can supply more detail verbally. It's fine to use the slides as a crutch to help you remember all the main points and the order in which you want to present them. However, if you need prompting to remember the extra details, then you do not have sufficient command of your material and need to practice your talk more before giving it publicly.

Just as you should not read text verbatim, you should not read diagrams verbatim. When discussing the architecture of a system, don't just read the names of the components or give low-level details about the interfaces between them. Rather, explain whatever is important, interesting, or novel about your decomposition; or discuss how the parts work together to achieve some goal that clients of the system care about; or use other techniques to give high-level understanding of the system rather than merely presenting a mass of low-level details.

(It's possible to overdo the practice of limiting what information appears on each slide, and you do want to have enough material to support you if there are questions or to show that the simplified model you presented verbally is an accurate generalization. But the mistake of including too much information is far more common.)

Text
------

Keep fonts large and easy to read from the back of the room. If something isn't important enough for your audience to be able to read, then it probably does not belong on your slides.

Use a sans-serif font for your slides. (Serifed fonts are best for reading on paper, but sans-serif fonts are easier to read on a screen.) PowerPoint's “Courier New” font is very light (its strokes are very thin). If you use it, always make it bold, then use color or underlining for emphasis where necessary.

When presenting code snippets, make sure the fonts is big enough to be readeable and only include the relevant bits.


Figures
---------

Make effective use of figures. Avoid a presentation that is just text. Such a presentation misses important opportunities to convey information. It is also is wearying to the audience.

Images and visualizations are extremely helpful to your audience. Include diagrams to show how your system works or is put together. Never include generic images, such as clip art, that don't relate directly to your talk. For example, if you have a slide about security, don't use the image of a padlock. As another example, when describing the problem your presentation solves, don't use an image of a person sitting at a computer looking frustrated. Just as good pictures and text are better than text alone, text alone is better than text plus bad pictures.

When you include a diagram on a slide, ensure that its background is the same color as that of the slide. For example, if your slides have a black background, then do not paste in a diagram with a white background, which is visually distracting, hard to read, and unattractive. You should invert the diagram so it matches the slide (which may require redrawing the diagram), or invert the slide background (e.g., use a white slide background) to match the diagrams.

Do not use eye candy such as transition effects, design elements that appear on every slide, or multi-color backgrounds. At best, you will distract the audience from the technical material that you are presenting. At worst, you will alienate the audience by giving them the impression that you are more interested in graphical glitz than in content. Your slides can be attractive and compelling without being fancy. Make sure that each element on the slides contributes to your message; if it does not, then remove it.

Color
-------

About 5% of American males are color-blind, so augment color with other emphasis where possible.

The presentation
==================

Make eye contact with the audience. This draws them in and lets you know whether you are going too fast, too slow, or just right. Do not face the screen, which puts your back to the audience. This is offputting, prevents you from getting feedback from the audience's body language, and can cause difficulty in hearing/understanding you. Do not look down at your computer, either, which shares many of the same problems.

Don't stand in front of the screen. This prevents the audience from viewing your slides.

Being animated is good, but do not pace. Pacing is very distracting, and it gives the impression that you are unprofessional or nervous.

When giving a presentation, never point at your laptop screen, which the audience cannot see. Amazingly, I have seen many people do this! Using a laser pointer is fine, but the laser pointer tends to shake, especially if you are nervous, and can be distracting. I prefer to use my hand, because the talk is more dynamic if I stride to the screen and use my whole arm; the pointing is also harder for the audience to miss. You must touch the screen physically, or come within an inch of it. If you do not touch the screen, most people will just look at the shadow of your finger, which will not be the part of the slide that you are trying to indicate.
If you find yourself suffering a nervous tic, such as saying “um” in the middle of every sentence, then practice more, including in front of audiences whom you do not know well.

If you get flustered, don't panic. One approach is to stop and regroup; taking a drink of water is a good way to cover this, so you should have water on hand even if you don't suffer from dry throat. Another approach is to just skip over that material; the audience is unlikely to know that you skipped something.


PyCon conference do not have a dress code. Simply make sure your articles of clothing do not have slogans
in breach of our `Code of Conduct`_. The most important thing is that you are comfortable with your clothing; if you are not, your discomfort will lead to a worse presentation.

.. _Code of Conduct: https://th.pycon.org/en/code-of-conduct/

Answering questions
=====================

Answering questions from the audience is very hard! Even after you become very proficient at giving a talk, it will probably take you quite a bit longer to become good at answering questions. So, don't feel bad if that part does not go perfectly, but do work on improving it.

Just as you practice your talk, practice answering questions — both the ones that you can predict, and also unpredictable ones. Giving practice talks to people who are willing to ask such questions can be very helpful.

When an audience member asks a question, it is a good idea to repeat the question, asking the questioner whether you have understood it, before answering the question. This has three benefits.

You ensure that you have understood the question. When thinking under pressure, it can be far too easy to jump to conclusions, and it is bad to answer a question different than the one that was asked. A related benefit is that you get to frame the question in your own words or from your own viewpoint.
You give yourself a few moments to think about your answer.
If the audience member does not have a microphone, the rest of the audience may not have been able to hear the question clearly.
Be willing to answer a question with “no” or “I don't know”. You will get into more trouble if you try to blather on or to make up an answer on the fly.


Practice talks
================

Always give a practice talk before you present in front of an audience. Even if you have read over your slides and think you know how the talk will go, when you speak out loud your ideas are likely to come out in a different or less clear way. (This is true about writing, too: even if you know what you want to say, it takes several revisions to figure out the best way to say it.) In fact, you should practice the talk to yourself — speaking out loud in front of a mirror, for example — before you give your first practice talk. In such a practice session, you must say every word you intend to in the actual talk, not skipping over any parts.

It can be a good idea to keep your practice talk audience relatively small — certainly fewer than 10 people. In a large group, many people won't bother to speak up. If the pool of potential attendees is larger than 10, you can give multiple practice talks, since the best feedback is given by someone who has not seen the talk (or even the material) before. Giving multiple practice talks is essential for high-profile talks such as conference talks and interview talks. Avoid a small audience of people you don't trust, who might be unanimous in a wrong opinion; getting a balance of opinions will help you avoid making too many mistakes in any one direction.

Consider videotaping yourself to see how you come across to others. This information can be a bit traumatic, but it is invaluable in helping you to improve.

When giving a practice talk, number your slides (say, in the corner), even if you don't intend to include slide numbers in your final presentation.

When giving a practice talk, it is very helpful to distribute hardcopy slides (remember to include slide numbers) so that others can easily annotate them and return them to you at the end of the talk. (Also, the audience will spend less time trying to describe what slide their comment applies to, and more time writing the comment and paying attention to you.) For non-practice talks, you generally shouldn't give out hardcopy slides, as they will tempt the audience to pay attention to the piece of paper instead of to you.

Go to other people's practice talks. This is good citizenship, and cultivating these obligations is a good way to ensure that you have an audience at your practice talk. Furthermore, attending others' talks can teach you a lot about good and bad talks — both from observing the speaker and thinking about how the talk can be better (or is already excellent), and from comparing the the feedback of audience members to your own opinions and observations. This does not just apply to practice talks: you should continually perform such introspective self-assessment.


