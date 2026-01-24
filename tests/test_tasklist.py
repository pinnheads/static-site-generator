import unittest
from src.core.enums import BlockType
from src.parser.block_parser import block_to_block_type, block_to_html


class TestTaskList(unittest.TestCase):
    def test_block_to_block_type_task_list(self):
        block = "- [ ] Task 1\n- [x] Task 2"
        self.assertEqual(block_to_block_type(block), BlockType.TASK_LIST)

    def test_block_to_html_task_list(self):
        block = "- [ ] Task 1\n- [x] Task 2"
        html_node = block_to_html(block, BlockType.TASK_LIST)
        
        self.assertEqual(html_node.tag, "ul")
        self.assertEqual(html_node.props["class"], "task-list")
        self.assertEqual(len(html_node.children), 2)
        
        # Check first item (unchecked)
        item1 = html_node.children[0]
        self.assertEqual(item1.tag, "li")
        self.assertEqual(item1.props["class"], "task-item")
        checkbox1 = item1.children[0]
        self.assertEqual(checkbox1.tag, "input")
        self.assertEqual(checkbox1.props["type"], "checkbox")
        self.assertTrue("disabled" in checkbox1.props)
        self.assertFalse("checked" in checkbox1.props)
        # Check text content of first item
        self.assertEqual(item1.children[1].value, "Task 1")

        # Check second item (checked)
        item2 = html_node.children[1]
        checkbox2 = item2.children[0]
        self.assertTrue("checked" in checkbox2.props)
        self.assertEqual(item2.children[1].value, "Task 2")

if __name__ == "__main__":
    unittest.main()
