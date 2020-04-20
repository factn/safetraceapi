#import <React/RCTBridgeModule.h>

@interface RCT_EXTERN_MODULE(MPCModule, NSObject)

RCT_EXTERN_METHOD(splitShares:(NSString *) sequence
                  resolver:(RCTPromiseResolveBlock) resolve
                  rejecter:(RCTPromiseRejectBlock) reject)

RCT_EXTERN_METHOD(joinShares:(NSArray *) shares
                  resolver:(RCTPromiseResolveBlock) resolve
                  rejecter:(RCTPromiseRejectBlock) reject)

@end
