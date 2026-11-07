#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2026 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)

from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/infinix/X6871',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
    'hardware/transsion',
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
}

blob_fixups: blob_fixups_user_type = {
    # Android 16 (AIDL era): the NDK/HIDL shims are no longer required.
    # The vendor blobs already reference the modern library sonames.

    # The neural-networks shim service must be enabled rather than started.
    'vendor/etc/init/android.hardware.neuralnetworks-shim-service-mtk.rc': blob_fixup()
        .regex_replace('start', 'enable'),

    # GNSS: the vendor blob links against the platform-only variant.
    ('vendor/bin/hw/android.hardware.gnss-service.mediatek',
     'vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so'): blob_fixup()
        .replace_needed('android.hardware.gnss-V1-ndk_platform.so',
                        'android.hardware.gnss-V1-ndk.so'),

    # Audio: the primary HAL uses the modern stagefright foundation library.
    'vendor/lib64/hw/audio.primary.mediatek.so': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so'),

    # Picture quality AIDL service.
    ('vendor/bin/hw/vendor.mediatek.hardware.pq_aidl-service',
     'vendor/lib64/hw/mt6895/vendor.mediatek.hardware.pq_aidl-impl.so'): blob_fixup()
        .add_needed('libbase_shim.so'),

    # Camera provider needs the metadata shim on Android 16.
    'vendor/lib64/hw/mt6895/android.hardware.camera.provider@2.6-impl-mediatek.so': blob_fixup()
        .add_needed('libcamera_metadata_shim.so'),

    # Sensor HAL: AIDL sensors service links against the shared converter.
    'vendor/lib64/hw/sensors.mediatek.V2.0.so': blob_fixup()
        .add_needed('android.hardware.sensors@1.0-convert-shared.so'),

    # Some vendor libraries still reference the 32-bit only symbol versions.
    ('vendor/lib64/mt6895/libneuralnetworks_sl_driver_mtk_prebuilt.so',
     'vendor/lib64/libtflite_mtk.so'): blob_fixup()
        .add_needed('libbase_shim.so'),

    # MTK RIL / IMS
    'vendor/bin/hw/mtkfusionrild': blob_fixup()
        .add_needed('libutils-v31.so'),

    # Process group shim for camera and composer
    ('vendor/lib64/mt6895/libcam.hal3a.so',
     'vendor/lib64/mt6895/libcam.hal3a.ctrl.so',
     'vendor/lib64/hw/hwcomposer.mtk_common.so'): blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'X6871',
    'infinix',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
