//
//  ViewController.swift
//  Notifier
//
//  Created by kang ki-hoon on 2017. 6. 11..
//  Copyright © 2017년 kang ki-hoon. All rights reserved.
//
import AWSCore
import AWSS3
import AWSCognito

import MobileCoreServices
import UIKit

class ViewController: UIViewController,UINavigationControllerDelegate, UIImagePickerControllerDelegate {
    private var Image: UIImage!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }
    override func viewDidAppear(_ animated: Bool) {
        
    }
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    func openPhotoLibrary(){
        let imagePicker = UIImagePickerController()
        if(UIImagePickerController.isSourceTypeAvailable(.photoLibrary)){
            imagePicker.sourceType = .photoLibrary
            imagePicker.delegate = self
            imagePicker.mediaTypes = [kUTTypeImage as String]
            imagePicker.allowsEditing = false
            present(imagePicker, animated: true, completion: nil)
        }
    }
    func openCamara(){
        let imagePicker = UIImagePickerController()
        if(UIImagePickerController.isSourceTypeAvailable(.camera)){
            imagePicker.sourceType = .camera
            imagePicker.delegate = self
            imagePicker.mediaTypes = [kUTTypeImage as String]
            imagePicker.allowsEditing = true
            present(imagePicker, animated: true, completion: nil)
        }
    }
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        picker.dismiss(animated: true,completion: nil)
        let pickedImage = info[UIImagePickerControllerOriginalImage] as? UIImage
        var data = UIImageJPEGRepresentation(pickedImage!,1.0)
        let transferUtil = AWSS3TransferUtility.default()
        var Timestamp: String {
            return "\(NSDate().timeIntervalSince1970 * 1000)"
        }
        transferUtil.uploadData(data!, bucket: "datasetfacerec", key: "friends/iOS-"+Timestamp+".jpg", contentType: "image/jpg", expression: nil, completionHandler: nil).continueWith{
            (task)->AnyObject! in if let error = task.error{
                self.ShowDebugLog.text = error.localizedDescription
            }
            return nil
        }
    }
    @IBAction func BtnAddAPhoto(_ sender: UIButton, forEvent event: UIEvent) {
        openPhotoLibrary()
    }
    @IBAction func BtnTakeAPhoto(_ sender: UIButton, forEvent event: UIEvent) {
        openCamara()
    }
    
    @IBOutlet weak var ShowDebugLog: UITextView!

}

