.. title: Schedule
.. slug: schedule
.. date: 2019-05-09 15:00:00 UTC+07:00
.. tags:
.. category:
.. link:
.. description: Conference schedule.
.. type: text

.. raw:: html

        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.js"></script>

        <style>
        .grid-container {
            width: 100%;
            display: grid;
            grid-template-columns: 60% auto;
            grid-row-gap: 10px;
        }

        .timeflex {
            display: flex;
            flex-direction: row;
        }

        @media screen and (max-width: 500px) /* Mobile */ {
            .timeflex {
                flex-direction: column;
            }
        }

        .schedule-item-container {
            display:flex;
            flex-direction: column;
        }

        .schedule-item {
            padding: 5px;
            padding-left: 10px;
            color: white;
            width: calc(100% - 20px);
            margin-bottom: 5px;
        }

        .schedule-item:hover, .workshop-item:hover {
          opacity: 0.8;
          cursor: pointer;
        }

        .schedule-item-1 {
            background-color: darkblue;
        }

        .schedule-item-2 {
            background-color: darkgreen;
        }

        .schedule-item-3 {
            background-color: darkred;
        }

        .schedule-item-5 {
            background-color: gray;
        }

        .p-5 {
            padding: 5px;
        }

        .workshop-item, .schedule-item-4 {
            grid-column-start:3;
            background-color: purple;
            color: white;
            margin-bottom: 5px;
            padding: 10px;
            margin-right: 5px;
        }

        .workshop-item .workshop-text {

        }

        .timetext {
            padding-top: 5px;
            padding-right: 5px;
        }

        a {
          color: white;
        }

        .hidden-field {
          display: none;
        }
        </style>

{{% schedule mode="schedule" file="../talks2019.yaml" talks_page="talks" speakers_page="speakers" %}}
