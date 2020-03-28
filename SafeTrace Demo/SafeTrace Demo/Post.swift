//
//  requests.swift
//  SafeTrace Demo
//
//  Created by Jack Hester on 3/25/20.
//  Copyright © 2020 SafeTrace API. All rights reserved.
//

import Foundation

/*
ROW TYPES:
0 = GPS Data
1 = BlueTooth Data
2 = Survey Data
*/

struct postPhone: Codable {
    let phone_number: Int
}

struct postLoc: Codable {
    let row_type: Int
    let user_id: Int
    let latitude: Double
    let longitude: Double
}

/*struct postBluetooth: Codable {
    let user_id: Int
    let row_type: Int
    let ...
}*/

struct postSymptoms: Codable {
    let user_id: Int
    let row_type: Int
    let symptoms: String
    let infection_status: Int
}
