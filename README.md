**Awda Project**  
A web-based platform designed to assist in locating missing and found individuals.

## Features

1. **QR Code Bracelet**:
    
    - A bracelet equipped with a QR code to help identify and guide individuals who are lost and unable to communicate their location.
2. **AI-Powered Location Suggestions**:
    
    - Provides intelligent location suggestions to aid those searching for missing individuals, utilizing data analysis and artificial intelligence.

## Proposal

The Awda application focuses on helping during critical moments—when someone is lost or searching for a missing individual. However, an additional feature could enhance its utility:

- **Proactive Tracking**:
    - By integrating hardware into the bracelet and connecting it to a phone, users could receive alerts when the tracked individual moves out of range. This feature uses Bluetooth Low Energy (BLE) technology to trigger alarms if proximity boundaries are breached.
    - Due to time constraints, this feature is currently not implemented but holds potential for future development.

## Technologies

### Core Technologies

1. **[Huawei RDS](https://support.huaweicloud.com/intl/en-us/rds/index.html)** with MySQL:
    
    - Manages and organizes data securely.
2. **[MindSpore](https://www.mindspore.cn/tutorials/en/master/beginner/introduction.html)**:
    
    - AI framework similar to TensorFlow for data analysis.
3. **[Huawei Cloud ECS](https://support.huaweicloud.com/intl/en-us/ecs/index.html)**:
    
    - Scalable web hosting for the platform.
4. **[Object Storage Service (OBS)](https://support.huaweicloud.com/intl/en-us/obs/index.html)**:
    
    - Secure storage for media files, including images and videos.
5. **[ModelArts](https://support.huaweicloud.com/intl/en-us/modelarts/index.html)**:
    
    - Facial recognition for photo matching.
6. **GPS & Location Services**:
    
    - **[Location Kit](https://developer.huawei.com/consumer/en/doc/HMSCore-Guides/dev-process-0000001050746141)**:
        - Tracks uploaded locations and enables geo-fencing to detect when devices enter, exit, or linger within specified geographic boundaries.

### Authentication & Security

1. **[IAM](https://support.huaweicloud.com/intl/en-us/iam/index.html)**:
    
    - Provides secure login with national ID verification and multi-factor authentication to prevent misuse.
2. **[Web Application Firewall (WAF)](https://support.huaweicloud.com/intl/en-us/waf/)**:
    
    - Protects sensitive data by mitigating cyber threats.

### Communication & Notifications

1. **[Simple Message Notification (SMN)](https://support.huaweicloud.com/intl/en-us/smn/index.html)**:
    - Sends SMS alerts for user verification and important notifications.

By combining cutting-edge technology with practical solutions, the Awda platform aims to provide a secure and reliable service for reconnecting lost individuals with their loved ones.