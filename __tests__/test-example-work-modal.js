import React from 'react';
import { shallow } from 'enzyme';
import ExampleWorkModal from '../js/example-work-modal';

import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

Enzyme.configure({ adapter: new Adapter() });

const myExample = {
    'title': "Work Example #1",
    'href': "https://example.com",
    'desc': "Lorem ipsum dolar sit amet, consectetur adipisicing elit etc.",
    'image': {
        'desc': "example screenshot of a project involving code",
        'src': "images/example1.png",
        'comment': ""
    }
};

describe("ExampleWorkModal component", () => {
    let component = shallow(<ExampleWorkModal example={myExample}/>);
    let anchors = component.find("a");

    it("Should contain a single 'a' element", () => {
        expect(anchors.length).toEqual(1);
    });

    it('Should link to our project', () => {
        expect(anchors.prop('href')).toEqual(myExample.href);
    });
});