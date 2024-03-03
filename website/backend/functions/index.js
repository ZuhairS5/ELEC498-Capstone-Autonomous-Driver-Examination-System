exports.callMLModel = (req, res) => {
    const userPassword = req.body.password;
    const hardcodedPassword = Buffer.from('Testing123').toString('base64');
  
    if (Buffer.from(userPassword).toString('base64') !== hardcodedPassword) {
      res.status(403).send('Incorrect password');
      return;
    }

    res.status(200).send('Password correct!');
};