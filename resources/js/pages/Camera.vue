<script lang="ts">
import { createComponent, computed, watch } from '@vue/composition-api'

import { useCamera } from '../use/camera'
import { useMicrophone } from '../use/microphone'
import { useSpeaker } from '../use/speaker'

export default createComponent({
  name: 'App',
  setup() {
    const { camera, cameras } = useCamera()
    const { microphone, microphones } = useMicrophone()
    const { speaker, speakers } = useSpeaker()

    // computed
    const camerasLabels = computed(() =>
      cameras.value.map(camera => camera.label)
    )

    // or method
    function getDevicesLabels(devices: MediaDeviceInfo[]) {
      return devices.map(device => device.label)
    }

    watch(cameras, value => {
      console.log(value)
    })

    return {
      camerasLabels,
      microphones,
      speakers,
      getDevicesLabels,
    }
  },
})
</script>

<template>
  <ul>
    <li>Connected cameras: {{ camerasLabels }}</li>
    <li>Connected microphones: {{ getDevicesLabels(microphones) }}</li>
    <li>Connected speakers: {{ getDevicesLabels(speakers) }}</li>
  </ul>
</template> 