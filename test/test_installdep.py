#---------------------------------------------------------------------------
# Copyright 2016 The Open Source Electronic Health Record Alliance
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#---------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from vivian_test_utils import setup_webdriver
import unittest
import re
import time

class test_installdep(unittest.TestCase):

  @classmethod
  def tearDownClass(cls):
    driver.quit()

  def test_02_packageAutocomplete(self):
    packageAuto = driver.find_element_by_id('package_autocomplete')
    installAuto = driver.find_element_by_id('install_autocomplete')

    packageName = "Registration"
    installVal  = "DG*5.3*397"
    packageAuto.clear()
    packageAuto.send_keys(packageName)
    time.sleep(1)
    for item in driver.find_elements_by_class_name('ui-menu-item'):
      if item.text == packageName:
        item.click()
        break
    time.sleep(1)

    installAuto.clear()
    installAuto.send_keys(installVal)
    time.sleep(1)
    for item in driver.find_elements_by_class_name('ui-menu-item'):
      if item.text == installVal:
        item.click()
        break
    time.sleep(1)

    foundVal = driver.find_elements_by_class_name('node')[-1].text
    self.assertTrue(installVal == foundVal, "Expected first node to be %s, found %s instead" % (installVal, foundVal))

  def test_04_panZoom(self):
    if browser == "FIREFOX":
      return # Test fails on FireFox, skip it for now

    patchTree = driver.find_element_by_id('treeview_placeholder').find_element_by_tag_name('g')
    oldTrans =  patchTree.get_attribute("transform")
    ActionChains(driver).move_to_element(patchTree).drag_and_drop_by_offset(patchTree, 100, -100).perform()
    time.sleep(1)
    self.assertNotEqual(oldTrans, patchTree.get_attribute("transform"), "Transform was the same after attempting drag and drop")
    oldTrans = patchTree.get_attribute("transform")

    ActionChains(driver).move_to_element_with_offset(patchTree, 10, 10).double_click(patchTree).perform()
    time.sleep(1)
    self.assertNotEqual(oldTrans, patchTree.get_attribute("transform"), "Transform was the same after attempting to zoom")

  def test_05_panCenter(self):
    if browser == "FIREFOX":
      return # Test fails on FireFox, skip it for now

    patchTree = driver.find_element_by_id('treeview_placeholder').find_element_by_tag_name('g')
    button = driver.find_element_by_xpath("//button[contains(@onclick,'_centerDisplay()')]")
    ActionChains(driver).move_to_element(patchTree).drag_and_drop_by_offset(patchTree, 100, -100).perform()
    oldVal = patchTree.get_attribute("transform")
    button.click()
    time.sleep(1)
    newVal = patchTree.get_attribute("transform")
    self.assertNotEqual(oldVal, newVal, "Centering the pan from drag-and-drop did not change the transform")

  def test_06_panReset(self):
    if browser == "FIREFOX":
      return # Test fails on FireFox, skip it for now

    patchTree = driver.find_element_by_id('treeview_placeholder').find_element_by_tag_name('g')
    ActionChains(driver).move_to_element(patchTree).drag_and_drop_by_offset(patchTree, 100, -100).perform()
    oldval = patchTree.get_attribute("transform")
    button = driver.find_element_by_xpath("//button[contains(@onclick,'_resetAllNode')]")
    button.click()
    time.sleep(1)
    newVal = patchTree.get_attribute("transform")
    self.assertNotEqual(oldval, newVal, "Reseting the pan from drag-and-drop did not change the transform")

  def test_07_node_highlighting(self):
    nodeList = driver.find_elements_by_class_name('node')
    ActionChains(driver).move_to_element(nodeList[-3]).perform()
    outlist = driver.find_elements_by_class_name("active")
    self.assertNotEqual(len(outlist), 0, "Unable to find an active node when hovering over item")

if __name__ == '__main__':
  description = "Test the install dependency tree page of the ViViaN(TM) webpage"
  page = "vivian/patchDependency.php"
  webroot, driver, browser = setup_webdriver(description, page)
  suite = unittest.TestLoader().loadTestsFromTestCase(test_installdep)
  unittest.TextTestRunner(verbosity=2).run(suite)
