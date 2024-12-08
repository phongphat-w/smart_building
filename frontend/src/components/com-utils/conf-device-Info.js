class ConfDeviceInfo {
    static devIdThermostats = '7c84b98d-8f69-4959-ac5b-1b2743077151';
    static devIdDemConVen = '080d460f-e54c-4262-a4ac-a3d42c40cbd5';
    static devIdBulbs = 'c0ec3c70-b76f-45e0-9297-8b5a4a462a47';
    static devIdElecMeter = 'f531b9c1-c46a-42c4-989d-1d5be315f6a6';
    static devIdPresence = '96b38698-d9ad-4355-807f-5580397471a1';
    static devIdBlinds = '69b29098-c768-423e-ac2e-cc443e18f8a9';
    static devIdAirCon = '3382ead3-4c22-4fac-bc92-d2cc11e94564';
    static devIdCameras = '2a66e85b-2e08-4a82-9617-f6ba6ab55cca';
    static devIdWaterLeak = '3e6448c0-eea1-4f8d-bfc1-366685232a83';
    static devIdBins = '2dcc0b13-ff3a-445d-b6c8-a92b05bbba6c';
    static devIdRfidTags = '21a0a6de-88a5-4a42-8734-1fa27483e138';
  
    static getAllDevices() {
      return {
        devIdThermostats: this.devIdThermostats,
        devIdDemConVen: this.devIdDemConVen,
        devIdBulbs: this.devIdBulbs,
        devIdElecMeter: this.devIdElecMeter,
        devIdPresence: this.devIdPresence,
        devIdBlinds: this.devIdBlinds,
        devIdAirCon: this.devIdAirCon,
        devIdCameras: this.devIdCameras,
        devIdWaterLeak: this.devIdWaterLeak,
        devIdBins: this.devIdBins,
        devIdRfidTags: this.devIdRfidTags,
      };
    }
  }
  
  export default ConfDeviceInfo;
  