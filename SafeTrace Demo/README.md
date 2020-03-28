# SafeTrace Demo Phone App

Proejct written as part of: <a href = "https://safetraceapi.org">https://safetraceapi.org</a>.  Code in this folder written by <a href="https://jackhester.com">Jack Hester</a>

## Overview

This folder contains the code for a basic iPhone app that will interface with the <a href="https://github.com/factn/safetraceapi/tree/master/RestAPI">SafeTrace Rest API</a>. The code is written in Swift 5.

## Current functionality

<strong>Entering new user</strong>
In its current state, the app is a simple single view iPhone app with a button to create a new user entry with a phone number. This works by submitting a phone number in the popup box presented after clicking the "Click Here" button under "Sign Up with Phone Number." After filling out the popup text field and clicking "submit," the phone nubmer will be inserted, along with an automatically generated user id, into the backend database. Information placed in the database via this method is NOT secured, so we advise that you DO NOT put any sensitive information in this field (including your real phone number).

<strong>Tracking location</strong>
In addition, the app will send the user's location data to the server at a pre-determiend time interval (currently set to every 60 seconds). No user action is required to activate this feature except for allowing location access when first opening the app. Please note: if you are using the iOS simulator, you need to set a location (can do so under the debug menu) in order for this to work.

<strong>Symptom entry</strong>
Similar to the new user entry, the user posts a text box

## Future functionality

<ul>
    <li>get/store the user id number on device, use this unique number for all other posts/requests (right now, user ids are hard-coded in for testing purposes)</li>
    <li>Form to enter (any known) infection status</li>
    <li>Bluetooth data collection and proximity detection</li>
    <li>Login functionality, storage of login info</li>
    <li>QR code scanner</li>
    <li>Make sure GPS works in background of devices (suspect this doesn't work on real device)</li>
</ul>

## How to use

To use this project, clone/download the repository and open the SafeTrace Demo in XCode. You can then click the "Build" (looks like play) button after selecting your desired device. Then, click into the simulator app, wich will open after a slight delay, where you can play around with the available features as they are added. For details on how to access the demo database, look at the code in the <a href="https://github.com/factn/safetraceapi/tree/master/RestAPI">Rest API</a> folder in this repository.

Please note: this app is currently desinged for backend testing purposes and is not guaranteed to work/display on all devices or simulators. It is also recommended that you go into settings > general > reset and click "reset location & privacy" before/after each run of the app, especially once the location and bluetooth functionality is implemented.
