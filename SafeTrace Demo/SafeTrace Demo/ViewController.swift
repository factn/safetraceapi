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

    override func viewDidLoad() {
        super.viewDidLoad()
        
        
        
        //self.view.backgroundColor = UIColor(hue: 0.5222, saturation: 0.63, brightness: 0.99, alpha: 1.0) /* #5de7fc */
        
        //get loc and permissions
        locationManager.requestAlwaysAuthorization()
        
        if CLLocationManager.locationServicesEnabled(){
            locationManager.delegate = self
            locationManager.desiredAccuracy = kCLLocationAccuracyBest
            locationManager.startUpdatingLocation()
        }
        
        //ensure location can run in background
        locationManager.allowsBackgroundLocationUpdates = true
        locationManager.pausesLocationUpdatesAutomatically = false
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

        phonePoster(post: phonePost) { (error) in
            if let error = error{
                fatalError(error.localizedDescription)
            }
        }
        
        }))
        
        self.present(alertController, animated: true)
    }
    
    // constant GPS monitoring (every 60s)
    // TODO: make sure this runs in background
    
    var startTime = Date()
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]){
        
        
        
        if let location = locations.first{
            
            let time = Date()
            
            let timeElapsed = time.timeIntervalSince(startTime)
            
            // only send to server every 60s, but phone gathers continuously due to method limitations
            if timeElapsed > 60{
                let lat = location.coordinate.latitude
                let long = location.coordinate.longitude
                    let phoneCoords = postLoc(row_type: 0, user_id: 1, latitude: lat, longitude: long)
                    postGPSInfo(post: phoneCoords) { (error) in
                        if let error = error{
                            fatalError(error.localizedDescription)
                        }
                    
                    }
                startTime = time
            }
                
        }
        
    }
    
    //update status and send to server
    @IBAction func testingController(_ sender: UISegmentedControl) {
        switch sender.selectedSegmentIndex{
        
        //unknown (1 on server)
        case 0:
            let testPost = postTest(user_id: 1, row_type: 2, symptoms: "", infection_status: 1)
            postTestStatus(post: testPost) { (error) in
                if let error = error{
                    fatalError(error.localizedDescription)
                }
            }
            
        //infected (2 on server)
        case 1:
            let testPost = postTest(user_id: 1, row_type: 2, symptoms: "", infection_status: 2)
            postTestStatus(post: testPost) { (error) in
                if let error = error{
                    fatalError(error.localizedDescription)
                }
            }
            
        //recovered (3 on server)
        case 2:
            let testPost = postTest(user_id: 1, row_type: 2, symptoms: "", infection_status: 3)
            postTestStatus(post: testPost) { (error) in
                if let error = error{
                    fatalError(error.localizedDescription)
                }
            }
            
        //user doesn't want to specify (0 on server)
        case 3:
            let testPost = postTest(user_id: 1, row_type: 2, symptoms: "", infection_status: 0)
            postTestStatus(post: testPost) { (error) in
                if let error = error{
                    fatalError(error.localizedDescription)
                }
            }
        default:
            break;
        }

    }
    
}
