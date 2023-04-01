import { useState, useEffect, useCallback} from 'react';
import { CSVLink, CSVDownload } from "react-csv";
import AssignmentTableService from '../../services/assignment-export-service'


const AssignmentExport = () =>  {
    //csvData = [
    //   ["courseID", "instructor", "student_email", "support_type"]
    //  ];
    let [data, setData] = useState([])
        
    useEffect(() => {
        const fetch_data = async () => {
            const res = await AssignmentTableService.get_assignment_table()
            setData(res.data)
            console.log(data)
        }
        fetch_data()
        .catch(console.error)
    }, [])
    
    return (
        <div>
            Started a file download

            {data.length !== 0 ? <CSVDownload data={data} target="_blank" fileName='assignment_table.csv'/>: null }
            
    
        </div>);
    
}

export default AssignmentExport;