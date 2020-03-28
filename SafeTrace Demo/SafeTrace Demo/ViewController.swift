//
//  ViewController.swift
//  SafeTrace Demo
//
//  Created by Jack Hester on 3/25/20.
//  Copyright © 2020 SafeTrace API. All rights reserved.
//

import UIKit
import CoreLocation

class ViewController: UIViewController, CLLocationManagerDelegate {
    
    
    let locationManager = CLLocationManager()
    private var startTime: Date?

    override func viewDidLoad() {
        super.viewDidLoad()
        
        
        
        //self.view.backgroundColor = UIColor(hue: 0.5222, saturation: 0.63, brightness: 0.99, alpha: 1.0) /* #5de7fc */
        
        //locationManager.requestWhenInUseAuthorization()
        locationManager.requestAlwaysAuthorization()
        
        if CLLocationManager.locationServicesEnabled(){
            locationManager.delegate = self
            locationManager.desiredAccuracy = kCLLocationAccuracyBest
            locationManager.startUpdatingLocation()
        }
  }
    
    //upload symptoms
    //TODO: add infection status to this (it's currently hard coded to 0)
    @IBAction func sendSymptoms(_ sender: Any) {
    
    
        let alertController = UIAlertController(title: "Enter Symptoms", message: "Please enter the symptoms you're experiencing", preferredStyle: .alert)
        alertController.addTextField { textfield in
            textfield.placeholder = "Cough, Fever"
        }
        
        alertController.addAction(UIAlertAction(title: "Cancel", style: .cancel, handler: nil))
        
        alertController.addAction(UIAlertAction(title: "Submit", style: .default, handler: { action in
                guard let text = alertController.textFields?.first?.text else {print("No text available"); return}
        
            let symptomPost = postSymptoms(user_id: 1, row_type: 2, symptoms: text, infection_status: 0)
        // NB: phonePost is in PostFunctions.swift
        postSymptomInfo(post: symptomPost) { (error) in
            if let error = error{
                fatalError(error.localizedDescription)
            }
        }
        
        }))
        
        self.present(alertController, animated: true)
    }
    
    //sign up with phone (just input phone number, proper signup not yet implemented on server side
    @IBAction func submitPhone(_ sender: Any) {
        let alertController = UIAlertController(title: "Sign Up", message: "Enter your Phone Number", preferredStyle: .alert)
        alertController.addTextField { textfield in
            textfield.placeholder = "Your phone number"
        }
        
        alertController.addAction(UIAlertAction(title: "Cancel", style: .cancel, handler: nil))
        
        alertController.addAction(UIAlertAction(title: "Submit", style: .default, handler: { action in
                guard let text = alertController.textFields?.first?.text else {print("No text available"); return}
        
        let txt_int = Int(text) ?? 0
        
        let phonePost = postPhone(phone_number: txt_int)
        // NB: phonePost is in PostFunctions.swift
        phonePoster(post: phonePost) { (error) in
            if let error = error{
                fatalError(error.localizedDescription)
            }
        }
        
        }))
        
        self.present(alertController, animated: true)
    }
    
    // constant GPS (every 60s)
    // TODO: make sure this runs in background
    // TODO: change from continuous passing of location to timed
    // https://stackoverflow.com/questions/41981255/timer-on-location-manager
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]){
        
        
        
        if let location = locations.first{
            let lat = location.coordinate.latitude
            let long = location.coordinate.longitude
                let phoneCoords = postLoc(row_type: 0, user_id: 1, latitude: lat, longitude: long)
                postGPSInfo(post: phoneCoords) { (error) in
                    if let error = error{
                        fatalError(error.localizedDescription)
                    }
                
                }
                /*do {
                    sleep(60)
                }*/
            //})
        }
        
    }
    

    
}
