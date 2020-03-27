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
    
    var locationManager: CLLocationManager?
    
    @IBOutlet weak var PhoneNumber: UITextField!
    
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        locationManager = CLLocationManager()
        
        locationManager?.delegate = self
    locationManager?.requestAlwaysAuthorization()
        
        //TODO: add feature so that full location is requested (must be tied to some action/request)

        //view.backgroundColor = .gray
        // Do any additional setup after loading the view.
    }
    
    
    @IBAction func submitPhone(_ sender: Any) {
        let alertController = UIAlertController(title: "Sign Up with Phone Number", message: "Enter your Phone Number", preferredStyle: .alert)
        alertController.addTextField { textfield in
            textfield.placeholder = "Your phone number"
        }
        
        alertController.addAction(UIAlertAction(title: "Cancel", style: .cancel, handler: nil))
        
        alertController.addAction(UIAlertAction(title: "Submit", style: .default, handler: { action in
                guard let text = alertController.textFields?.first?.text else {print("No text available"); return}
        
        let txt_int = Int(text) ?? 0
        
        let phonePost = Post(phone_number: txt_int)
        // NB: postUserPhone is in Requests.swift
        postUserPhone(post: phonePost) { (error) in
            if let error = error{
                fatalError(error.localizedDescription)
            }
        }
        
        }))
        
        self.present(alertController, animated: true)
    }
}

