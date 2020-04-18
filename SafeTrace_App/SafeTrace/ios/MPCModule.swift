import Foundation

@objc(MPCModule)
class MPCModule : NSObject {
  
  @objc(splitShares:resolver:rejecter:)
  func splitShares(_ sequence: String, resolver resolve: RCTPromiseResolveBlock, rejecter reject:RCTPromiseRejectBlock) {
    resolve(true);
  }
  
  @objc(joinShares:resolver:rejecter:)
   func joinShares(_ shares: NSArray, resolver resolve: RCTPromiseResolveBlock, rejecter reject:RCTPromiseRejectBlock) {
     resolve(true);
   }
  
}
