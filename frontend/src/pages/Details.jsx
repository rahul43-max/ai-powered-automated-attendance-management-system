import React from 'react';
import Navbar from '../components/Navbar';

const Details = () => {
  return (
    <div className="min-h-screen flex flex-col bg-[#f4f4f4]">
      <Navbar />
      
      <div className="flex-1 p-2">
        <div className="tkrec-card max-w-7xl mx-auto p-4 bg-white mt-2">
          
          {/* Header Section */}
          <div className="text-center mb-4 border-b pb-4">
            <h1 className="text-2xl font-bold text-[#b71c1c]">
              TEEGALA KRISHNA REDDY ENGINEERING COLLEGE
            </h1>
            <p className="text-xs font-semibold">(UGC-AUTONOMOUS)</p>
            <p className="text-[10px] text-gray-600 mb-2">
              (Sponsored by TKR Educational Society, Approved by AICTE, Affiliated to JNTUH Accredited by NAAC & NBA)<br />
              Medbowli, Meerpet, Balapur(M), Hyderabad, Telangana - 500097
            </p>
            <div className="bg-[#f2ecec] p-1 font-bold text-sm text-gray-800 border">
              Panjugula Rahul - Admission Details (AY : 2023-24) - 23R91A05P1 - B.Tech - CSE
            </div>
          </div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            {/* Left Column */}
            <div className="space-y-4">
              
              {/* Personal Details */}
              <div>
                <div className="tkrec-red-header text-center bg-[#ffeaea] text-black font-semibold border p-1">
                  Personal Details
                </div>
                <table className="tkrec-table w-full text-left">
                  <tbody>
                    <tr><th className="w-1/3">Student Name :</th><td className="w-2/3 font-semibold">Panjugula Rahul</td><td rowSpan="4" className="w-24 text-center"><div className="w-20 h-24 bg-blue-200 mx-auto border"><img src="https://via.placeholder.com/80x100" alt="Student" className="w-full h-full object-cover" /></div></td></tr>
                    <tr><th>Father Name :</th><td>P.Ashok</td></tr>
                    <tr><th>Mother Name :</th><td></td></tr>
                    <tr><th>Date of Birth :</th><td>20-09-2003</td></tr>
                    <tr><th>Gender :</th><td>Male</td><th>Student Mobile :</th><td>6302771583</td></tr>
                    <tr><th>Parent Mobile :</th><td>9912961798</td><th>Mother Mobile :</th><td></td></tr>
                    <tr><th>Caste :</th><td>OC</td><th>Sub Caste :</th><td></td></tr>
                    <tr><th>Religion :</th><td></td><th>PH Status :</th><td></td></tr>
                    <tr><th>Annual Income :</th><td></td><th>Identity Mark1 :</th><td></td></tr>
                    <tr><th>Identity Mark2 :</th><td></td><th>Aadhaar Number :</th><td></td></tr>
                    <tr><th>Email :</th><td colSpan="3"></td></tr>
                  </tbody>
                </table>
              </div>

              {/* Address */}
              <div>
                <div className="tkrec-red-header text-center bg-[#ffeaea] text-black font-semibold border p-1">
                  Address for Communication
                </div>
                <table className="tkrec-table w-full text-left">
                  <tbody>
                    <tr><th className="w-1/4">Door No :</th><td className="w-1/4"></td><th className="w-1/4">Town / Village :</th><td className="w-1/4"></td></tr>
                    <tr><th>Street :</th><td></td><th>District :</th><td></td></tr>
                    <tr><th>Mandal :</th><td></td><th>Pincode :</th><td></td></tr>
                    <tr><th>State :</th><td colSpan="3"></td></tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* Right Column */}
            <div className="space-y-4">
              
              {/* Educational Details */}
              <div>
                <div className="tkrec-red-header text-center bg-[#ffeaea] text-black font-semibold border p-1">
                  Educational Details
                </div>
                <table className="tkrec-table w-full text-left">
                  <tbody>
                    <tr><th className="w-1/2">SSC Hallticket No :</th><td className="w-1/2"></td><th className="w-1/4 border-l-0 text-right pr-2">SSC CGP / GP :</th><td></td></tr>
                    <tr><th>Inter Hallticket No :</th><td></td><th className="border-l-0 text-right pr-2">Inter CGP / GP :</th><td></td></tr>
                    <tr><th>Degree Hallticket No :</th><td></td><th className="border-l-0 text-right pr-2">Degree CGP / GP :</th><td></td></tr>
                    <tr><th>UG Hallticket No :</th><td></td><th className="border-l-0 text-right pr-2">UG CGP / GP :</th><td></td></tr>
                  </tbody>
                </table>
              </div>

              {/* Admission Details */}
              <div>
                <div className="tkrec-red-header text-center bg-[#ffeaea] text-black font-semibold border p-1">
                  Admission Details
                </div>
                <table className="tkrec-table w-full text-left">
                  <tbody>
                    <tr><th className="w-1/3">Admitted Under :</th><td className="w-1/3">Convener</td><th className="w-1/6">CET :</th><td></td></tr>
                    <tr><th>CET Rollno :</th><td></td><th>CET Rank :</th><td>0</td></tr>
                  </tbody>
                </table>
              </div>

              {/* Documents Uploaded */}
              <div>
                <div className="tkrec-red-header text-center bg-[#ffeaea] text-black font-semibold border p-1">
                  Documents uploaded
                </div>
                <table className="tkrec-table w-full text-left">
                  <tbody>
                    <tr><th className="w-1/4">6th to 10th Bonafide :</th><td className="w-1/4 font-semibold">No</td><th className="w-1/4">SSC Long Memo :</th><td className="w-1/4 font-semibold">No</td></tr>
                    <tr><th>Inter Long Memo :</th><td className="font-semibold">No</td><th>Inter Bonafide :</th><td className="font-semibold">No</td></tr>
                    <tr><th>Latest TC :</th><td className="font-semibold">No</td><th>Caste Certificate :</th><td className="font-semibold">No</td></tr>
                    <tr><th>ROC :</th><td className="font-semibold">No</td><th>Joining Receipt :</th><td className="font-semibold">No</td></tr>
                    <tr><th>Allotment Order :</th><td className="font-semibold">No</td><th>CET Hall Ticket :</th><td className="font-semibold">No</td></tr>
                    <tr><th>CET Rank Card :</th><td className="font-semibold">No</td><th>EWS Certificate :</th><td className="font-semibold">No</td></tr>
                    <tr><th>Income Certificate :</th><td className="font-semibold">No</td><th>Aadhaar Card :</th><td className="font-semibold">No</td></tr>
                    <tr><th>Passport Size Photo :</th><td className="font-semibold">Yes</td><th>Signature :</th><td className="font-semibold">No</td></tr>
                  </tbody>
                </table>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Details;
