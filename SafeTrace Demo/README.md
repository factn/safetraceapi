# SafeTrace Demo Phone App

Project written as part of: <a href = "https://safetraceapi.org">https://safetraceapi.org</a>.  Code in this folder written by <a href="https://jackhester.com">Jack Hester</a>

## Overview

This folder contains the code for a basic iPhone app that will interface with the <a href="https://github.com/factn/safetraceapi/tree/master/RestAPI">SafeTrace Rest API</a>. The code is written in Swift 5.

## Current functionality

In its current state, the app is a simple single view iPhone app with a button to create a new user entry with a phone number. This works by submitting a phone number in the popup box presented after clicking the "Click Here" button under "Sign Up with Phone Number." After filling out the popup text field and clicking "submit," the phone nubmer will be inserted, along with an automatically generated user id, into the backend database. Information placed in the database via this method is NOT secured, so we advise that you DO NOT put any sensitive information in this field (including your real phone number).

## Future functionality

<ul>
    <li>Form to enter symptoms</li>
    <li>Form to enter (any known) infection status</li>
    <li>GPS location monitoring</li>
    <li>Bluetooth data collection and proximity detection</li>
    <li>Login functionality, storage of login info</li>
    <li>QR code scanner</li>
</ul>

## How to use

To use this project, clone/download the repository and open the SafeTrace Demo in XCode. You can then click the "Build" (looks like play) button after selecting your desired device. Then, click into the simulator app, wich will open after a slight delay, where you can play around with the available features as they are added. For details on how to access the demo database, look at the code in the <a href="https://github.com/factn/safetraceapi/tree/master/RestAPI">Rest API</a> folder in this repository.

Please note: this app is currently desinged for backend testing purposes and is not guaranteed to work/display on all devices or simulators. It is also recommended that you go into settings > general > reset and click "reset location & privacy" before/after each run of the app, especially once the location and bluetooth functionality is implemented.
