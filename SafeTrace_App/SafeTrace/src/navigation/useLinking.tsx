import { useLinking } from '@react-navigation/native';

export default (containerRef: any) => {
  return useLinking(containerRef, {
    prefixes: ['/'],
  });
}
