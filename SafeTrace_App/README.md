# SafeTrace App

This is the frontend mobile app for SafeTrace API (see <a href="https://safetraceapi.org">our website</a>).

>#
This app is still under development and NOT ready to be used by the general public!
>#

## Overview

This app is written in React Native using Expo. It is a tabbed app and will have a home tab, a notificaton and contact information tab, and a privacy/data tab. 

## Usage

You can run this app for simulation purposes using <a href="https://expo.io">Expo</a>.
>#
PLEASE NOTE: app.json is missing in the root (SafeTrace) directory. This is becasue it includes a secret api key. To use this, you will need to add the app.json file (there is a template in this SafeTrace_App directory) and then fill in your own API key, wich you can get via command line using <a href="https://github.com/factn/safetraceapi/blob/master/api/README.md#create-account">the instructions in this readme</a>.
>#

## Current functionality

This app currently:<br>
<ul>
    <li>Registers a new user (Sign Up button)</li>
    <li>Allows for a device to be removed/unregistered</li>
    <li>Does the first step of submitting symptom data (sends first POST request and gets back encrypted data, but does not yet send encrypted data to storage)</li>
<ul>


## TODOs

The next tasks include:
<ul>
    <li>Finishing the symptom submission function</li>
    <li>Adding testing status input/functionality</li>
    <li>(Securely) storing the user's private key in device storage</li>
    <li>Implementing GPS tracking</li>
    <li>Implementing Bluetooth tracking</li>
    <li>(Optional) Implemting WiFi tracking</li>
    <li>Push notification functionality</li>
    <li>Data use requests</li>
    <li>Contact and data request info</li>
    <li>Various images, UI elements, and privacy statements/terms of use</li>
<ul>
